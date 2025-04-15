import asyncio
import base64
import pathlib
import re

import aiohttp
import django.conf
import django.core
import django.core.exceptions
import django.db.models
import django.dispatch
import PIL.Image
import stickers.constants
import stickers.managers
import tg_bot.bot
import transliterate


class StickerPack(django.db.models.Model):
    name = django.db.models.CharField('name')
    slug = django.db.models.SlugField('slug', unique=True)
    published_on_tg = django.db.models.BooleanField(
        'published_on_tg',
        default=False,
    )

    def save(self, *args, **kwargs):
        text = self.name
        for k, v in stickers.constants.LOOKALIKES.items():
            text = text.replace(k, v)

        text = text.lower().replace(' ', '')
        self.slug = transliterate.translit(text, 'ru', reversed=True)
        return super().save(*args, **kwargs)


class Sticker(django.db.models.Model):
    objects = stickers.managers.StickerManager()

    image = django.db.models.ImageField(
        'sticker_image',
        upload_to='stickers/just_img/',
    )
    image_for_tg = django.db.models.ImageField('sticker_image', upload_to='stickers/for_tg/', blank=True)
    decryption = django.db.models.TextField('decryption')
    file_id_from_tg = django.db.models.CharField('file_id_from_tg', blank=True, null=True)
    stickerpack = django.db.models.ForeignKey(
        StickerPack, on_delete=django.db.models.CASCADE, related_name='sticker', default=None
    )

    def clean(self):
        if not self.image.path.split('.')[-1].lower() in stickers.constants.IMAGE_EXTENSIONS:
            raise django.core.exceptions.ValidationError('формат файла с изображением некорректен')

        return super().clean()


def get_cleaned_text_without_time(text: str) -> str:
    return re.sub(r'\b\d{1,2}:\d{2}\b', '', text).strip()


async def make_ocr_request(session, base64_image, file_extension, language):
    data = {
        'apikey': django.conf.settings.OCR_SPACE_APIKEY,
        'base64Image': f'data:image/{file_extension};base64,{base64_image}',
        'language': language,
    }
    async with session.post('https://api.ocr.space/parse/image', data=data) as response:
        response = await response.json()
        return response


@django.dispatch.receiver(django.db.models.signals.post_save, sender=Sticker)
async def add_decryption(sender, instance, created, **kwargs):
    file_extension = instance.image.path.split('.')[-1]
    with pathlib.Path(instance.image.path).open('rb') as image_file:
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')

    async with aiohttp.ClientSession() as session:
        tasks = [
            make_ocr_request(session, base64_image, file_extension, 'rus'),
            make_ocr_request(session, base64_image, file_extension, 'eng'),
        ]
        results = await asyncio.gather(*tasks)
        jsoned_text_rus, jsoned_text_eng = results

    text = ' '.join(list(map(lambda x: x['ParsedText'], jsoned_text_rus['ParsedResults']))) + ' '.join(
        list(map(lambda x: x['ParsedText'], jsoned_text_eng['ParsedResults']))
    )
    text = text.replace('\r', ' ').replace('\n', '')
    img = PIL.Image.open(instance.image.path).convert('RGBA')
    background = PIL.Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    width, height = img.size
    if width > height:
        new_width = 512
        new_height = int(height * (512 / width))
    else:
        new_height = 512
        new_width = int(width * (512 / height))

    img = img.resize((new_width, new_height), PIL.Image.LANCZOS)
    x = (512 - img.width) // 2
    y = (512 - img.height) // 2
    background.paste(img, (x, y), img)
    output_path = instance.image.path.rsplit('.', 1)[0] + '.webp'
    background.save(output_path, 'webp', quality=99)
    image_field = 'for_tg/'.join(output_path.split('media/')[-1].split('just_img/'))
    file_id = await tg_bot.bot.add_sticker_to_stickerpack(instance.image.path, instance.stickerpack.slug)
    await sender.objects.filter(id=instance.id).aupdate(
        decryption=get_cleaned_text_without_time(text),
        image_for_tg=image_field,
        file_id_from_tg=file_id,
    )


@django.dispatch.receiver(django.db.models.signals.pre_delete, sender=Sticker)
def delete_sticker_from_tg_stickerpack(sender, instance, created, **kwargs):
    pass


@django.dispatch.receiver(django.db.models.signals.post_save, sender=StickerPack)
async def add_stickerpack_to_tg(sender, instance, created, **kwargs):
    await tg_bot.bot.create_stickerpack(instance.name, instance.slug,
                                        Sticker.objects.get_stickers_by_stickerpack(instance))

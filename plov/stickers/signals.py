import aiohttp
import asyncio
import base64
import io
import pathlib
import PIL
import re

import django.conf
import django.db.models.signals

import stickers.models
import tg_bot.bot


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


@django.dispatch.receiver(django.db.models.signals.post_save, sender=stickers.models.Sticker)
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
    width, height = img.size
    if width > height:
        new_width = 512
        new_height = int(height * (512 / width))
    else:
        new_height = 512
        new_width = int(width * (512 / height))

    img = img.resize((new_width, new_height), PIL.Image.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, 'webp', quality=99)
    file_id = await tg_bot.bot.add_sticker_to_stickerpack(buffer, instance.stickerpack.slug)
    await sender.objects.filter(id=instance.id).aupdate(
        decryption=get_cleaned_text_without_time(text),
        image_for_tg=buffer,
        file_id_from_tg=file_id,
    )
    buffer.close()


@django.dispatch.receiver(django.db.models.signals.pre_delete, sender=stickers.models.Sticker)
async def delete_sticker_from_tg_stickerpack(sender, instance, **kwargs):
    await tg_bot.bot.delete_sticker_from_stickerpack(instance.file_id_from_tg)


@django.dispatch.receiver(django.db.models.signals.post_save, sender=stickers.models.StickerPack)
async def add_stickerpack_to_tg(sender, instance, created, **kwargs):
    if not instance.published_on_tg:
        await tg_bot.bot.create_stickerpack(instance.name, instance.slug,
                                            stickers.models.Sticker.objects.get_stickers_by_stickerpack(instance))
        await sender.objects.filter(id=instance.id).aupdate(
            published_on_tg=True
        )

import django.core.exceptions
import django.db.models
import transliterate

import stickers.constants
import stickers.managers


class StickerPack(django.db.models.Model):
    name = django.db.models.CharField('name')
    slug = django.db.models.SlugField('slug', unique=True)
    published_on_tg = django.db.models.BooleanField(
        'published_on_tg',
        default=False,
    )

class Sticker(django.db.models.Model):
    objects = stickers.managers.StickerManager()

    image = django.db.models.ImageField(
        'sticker_image',
        upload_to='stickers/just_img/',
    )
    image_for_tg = django.db.models.ImageField('sticker_image', upload_to='stickers/for_tg/', blank=True)
    decryption = django.db.models.TextField(blank=True)
    file_id_from_tg = django.db.models.CharField('file_id_from_tg', blank=True, null=True)
    stickerpack = django.db.models.ForeignKey(
        StickerPack,
        on_delete=django.db.models.CASCADE,
        related_name='sticker',
        default=None,
    )

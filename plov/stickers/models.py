import django.db.models

import stickers.managers


class StickerPack(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name='Название набора',
        max_length=100,
        help_text='Уникальное название набора стикеров',
    )
    slug = django.db.models.SlugField(
        verbose_name='URL-идентификатор',
        unique=True,
        max_length=100,
        help_text='Уникальная часть URL для набора стикеров (только латинские буквы, цифры, дефисы и подчёркивания)',
    )
    published_on_tg = django.db.models.BooleanField(
        verbose_name='Опубликовано в Telegram',
        default=False,
        help_text='Отметьте, если набор опубликован в Telegram',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Набор стикеров'
        verbose_name_plural = 'Наборы стикеров'

    def __str__(self):
        return self.name


class Sticker(django.db.models.Model):
    objects = stickers.managers.StickerManager()

    image = django.db.models.ImageField(
        verbose_name='Изображение стикера',
        upload_to='stickers/just_img/',
        help_text='Основное изображение стикера (рекомендуемый размер: 512x512 px)',
    )
    image_for_tg = django.db.models.ImageField(
        verbose_name='Изображение для Telegram',
        upload_to='stickers/for_tg/',
        blank=True,
        help_text='Оптимизированная версия стикера для Telegram (формат WEBP, размер до 512 KB)',
    )
    decryption = django.db.models.TextField(
        verbose_name='Описание стикера',
        blank=True,
        help_text='Текстовое описание или ключевые слова для стикера',
    )
    file_id_from_tg = django.db.models.CharField(
        verbose_name='ID файла в Telegram',
        blank=True,
        null=True,
        max_length=100,
        help_text='Уникальный идентификатор стикера в Telegram после публикации',
    )
    stickerpack = django.db.models.ForeignKey(
        'stickers.StickerPack',
        verbose_name='Набор стикеров',
        on_delete=django.db.models.CASCADE,
        related_name='stickers',
        default=None,
        help_text='Набор, к которому принадлежит этот стикер',
    )

    class Meta:
        ordering = ['stickerpack', 'id']
        verbose_name = 'Стикер'
        verbose_name_plural = 'Стикеры'

    def __str__(self):
        return f'Стикер из набора "{self.stickerpack.name}"'

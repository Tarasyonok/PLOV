import pathlib

import django.conf
import telegram
import telegram.constants


async def create_stickerpack(stickerpack_name, stickerpack_slug, stickers_img_paths):
    bot = telegram.Bot(django.conf.settings.TG_BOT_TOKEN)
    user_id = django.conf.settings.TG_USER_ID
    stickers = []
    with pathlib.Path('tg_bot/django.png').open('rb') as f:
        sticker = telegram.InputSticker(
            sticker=f.read(),
            emoji_list=['😀'],
            format=telegram.constants.StickerFormat.STATIC,
        )
        stickers.append(sticker)

    await bot.create_new_sticker_set(
        user_id=user_id,
        name=stickerpack_slug + django.conf.settings.TG_STICKERPACK_ENDING,
        title=stickerpack_name,
        stickers=stickers,
    )


async def add_sticker_to_stickerpack(buffer, stickerpack_slug):
    bot = telegram.Bot(django.conf.settings.TG_BOT_TOKEN)
    user_id = django.conf.settings.TG_USER_ID
    buffer.seek(0)
    sticker = telegram.InputSticker(
        sticker=buffer.read(),
        emoji_list=['😀'],
        format=telegram.constants.StickerFormat.STATIC,
    )

    stickerpack_name = stickerpack_slug + django.conf.settings.TG_STICKERPACK_ENDING

    await bot.add_sticker_to_set(
        user_id=user_id,
        name=stickerpack_name,
        sticker=sticker,
    )
    stickerset = await bot.get_sticker_set(stickerpack_name)
    return stickerset.stickers[-1].file_id


async def delete_sticker_from_stickerpack(file_id):
    bot = telegram.Bot(django.conf.settings.TG_BOT_TOKEN)
    await bot.delete_sticker_from_set(file_id)

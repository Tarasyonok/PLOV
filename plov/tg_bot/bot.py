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
            format=telegram.constants.StickerFormat.STATIC
        )
        stickers.append(sticker)

    await bot.create_new_sticker_set(
        user_id=user_id,
        name=stickerpack_slug + django.conf.settings.TG_STICKERPACK_ENDING,
        title=stickerpack_name,
        stickers=stickers,
    )


async def add_sticker_to_stickerpack(sticker_img_path, stickerpack_slug):
    bot = telegram.Bot(django.conf.settings.TG_BOT_TOKEN)
    user_id = django.conf.settings.TG_USER_ID
    print(stickerpack_slug)
    with pathlib.Path(sticker_img_path).open('rb') as f:
        sticker = (
            telegram.InputSticker(
                sticker=f.read(),
                emoji_list=['😀'],
                format=telegram.constants.StickerFormat.STATIC
            )

        )

    stickerpack_name = stickerpack_slug + django.conf.settings.TG_STICKERPACK_ENDING

    bot.add_sticker_to_set(
        user_id=user_id,
        name=stickerpack_name,
        sticker=sticker,
    )
    stickerset = await bot.get_sticker_set(stickerpack_name)
    return stickerset.stickers[-1].file_id

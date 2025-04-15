import django.contrib.admin
import stickers.models


class StickerInline(django.contrib.admin.TabularInline):
    model = stickers.models.Sticker
    readonly_fields = (stickers.models.Sticker.decryption.field.name,)
    extra = 1


@django.contrib.admin.register(stickers.models.StickerPack)
class StickerPackAdmin(django.contrib.admin.ModelAdmin):
    list_display = (stickers.models.StickerPack.name.field.name, stickers.models.StickerPack.slug.field.name)
    fields = (stickers.models.StickerPack.name.field.name,)
    inlines = (StickerInline,)

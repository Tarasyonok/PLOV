import django.contrib.admin

import stickers.models


class StickerInline(django.contrib.admin.TabularInline):
    model = stickers.models.Sticker
    readonly_fields = ('decryption',)
    extra = 1


@django.contrib.admin.register(stickers.models.StickerPack)
class StickerPackAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('name', 'slug')
    fields = ('name',)
    inlines = (StickerInline,)

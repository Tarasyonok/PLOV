import django.conf
import django.urls
import django.views.generic

import stickers.models


class AddStickerPackView(django.views.generic.CreateView):
    model = stickers.models.StickerPack
    template_name = 'stickers/add_sticker_pack.html'
    fields = ['name']

    def get_success_url(self):
        return django.urls.reverse('stickers:stickerpackinfo', kwargs={'pk': self.object.pk})


class StickerPackDetailView(django.views.generic.DetailView):
    model = stickers.models.StickerPack
    template_name = 'stickers/stickerpack_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stickers'] = stickers.models.Sticker.objects.get_stickers_by_stickerpack(self.object)
        context['url_to_tg'] = django.conf.settings.TG_START_OF_TG_URL_ON_STICKERPACK + self.object.slug + django.conf.settings.TG_STICKERPACK_ENDING
        return context


class AddStickerView(django.views.generic.CreateView):
    model = stickers.models.Sticker
    template_name = 'stickers/add_sticker.html'
    fields = ['image']

    def form_valid(self, form):
        stickerpack_id = self.kwargs.get('stickerpack_id')
        stickerpack = stickers.models.StickerPack.objects.get(pk=stickerpack_id)
        sticker = form.save(commit=False)
        sticker.stickerpack = stickerpack
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse('stickers:stickerpackinfo', kwargs={'pk': self.kwargs.get('stickerpack_id')})

class DeleteStickerView(django.views.generic.DeleteView):
    model = stickers.models.Sticker

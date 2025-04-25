import django.conf
import django.shortcuts
import django.urls
import django.views.generic
import elasticsearch_dsl
import transliterate

import stickers.models
import stickers.utils.constants
import stickers.utils.documents


class AddStickerPackView(django.views.generic.CreateView):
    model = stickers.models.StickerPack
    template_name = 'stickers/add_sticker_pack.html'
    fields = ['name']

    def form_valid(self, form):
        text = form.cleaned_data['name']
        for k, v in stickers.utils.constants.LOOKALIKES.items():
            text = text.replace(k, v)

        text = text.lower().replace(' ', '')
        slug_generated = transliterate.translit(text, 'ru', reversed=True)
        if stickers.models.StickerPack.objects.filter(slug=slug_generated).exists():
            form.add_error('name', 'Уже есть похожее на это название стикерпака')
            return self.form_invalid(form)

        self.object = form.save(commit=False)
        self.object.slug = slug_generated
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse('stickers:stickerpackinfo', kwargs={'pk': self.object.pk})


class StickerPackDetailView(django.views.generic.DetailView):
    model = stickers.models.StickerPack
    template_name = 'stickers/stickerpack_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stickers'] = stickers.models.Sticker.objects.get_stickers_by_stickerpack(self.object)
        context['url_to_tg'] = (
            django.conf.settings.TG_START_OF_TG_URL_ON_STICKERPACK
            + self.object.slug
            + django.conf.settings.TG_STICKERPACK_ENDING
        )
        return context


class StickerpackList(django.views.generic.ListView):
    model = stickers.models.StickerPack
    template_name = 'stickers/stickerpack_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stickerpacks'] = stickers.models.StickerPack.objects.all()
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
        try:
            sticker.full_clean()
        except django.core.exceptions.ValidationError as e:
            for field, errors in e.error_dict.items():
                for error in errors:
                    form.add_error(field, error)

            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse('stickers:stickerpackinfo', kwargs={'pk': self.kwargs.get('stickerpack_id')})


class DeleteStickerView(django.views.generic.DeleteView):
    model = stickers.models.Sticker
    template_name = 'stickers/delete_sticker.html'

    def get_success_url(self):
        return django.urls.reverse('stickers:stickerpackinfo', kwargs={'pk': self.kwargs.get('stickerpack_id')})


class SearchStickerView(django.views.generic.ListView):
    model = stickers.models.Sticker
    template_name = 'stickers/search_sticker.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        text = self.request.GET.get('q')
        q = elasticsearch_dsl.Q(
            'multi_match',
            query=text,
            fields=[
                'decryption',
            ],
            fuzziness='auto',
        )
        search = stickers.utils.documents.StickerDocument.search().query(q)
        context['objects'] = search.to_queryset()
        return context


class SetLikeOnSticker(django.views.View):
    def post(self, request, pk):
        sticker = django.shortcuts.get_object_or_404(stickers.models.Sticker, pk=pk)
        user = request.user
        liked = True
        if sticker in user.profile.featured_stickers.all():
            user.profile.featured_stickers.remove(sticker)
            liked = False
        else:
            user.profile.featured_stickers.add(sticker)

        user.profile.save()
        return django.shortcuts.render(request, 'stickers/button.html', {'sticker': sticker, 'liked': liked})

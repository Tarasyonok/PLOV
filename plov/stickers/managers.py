import django.apps
import django.db.models


class StickerManager(django.db.models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fields_initialized = False
        self._model_cache = {}

    def _get_model(self, app_label, model_name):
        if (app_label, model_name) not in self._model_cache:
            self._model_cache[(app_label, model_name)] = django.apps.apps.get_model(
                app_label,
                model_name,
            )

        return self._model_cache[(app_label, model_name)]

    def _init_fields(self):
        if not self._fields_initialized:
            sticker = self._get_model('stickers', 'Sticker')

    def get_queryset(self):
        self._init_fields()
        return super().get_queryset()

    def get_stickers_by_stickerpack(self, stickerpack_obj):
        queryset = self.get_queryset()
        queryset_filtered = queryset.filter(
            stickerpack=stickerpack_obj
        )
        return queryset_filtered
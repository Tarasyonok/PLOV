import importlib

from django.apps import AppConfig


class StickersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stickers'
    verbose_name = 'Стикеры'

    def ready(self):
        importlib.import_module('stickers.utils.signals')

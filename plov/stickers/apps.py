from django.apps import AppConfig


class StickersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stickers'

    def ready(self):
        import stickers.signals

import importlib

import django.apps


class UsersConfig(django.apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        importlib.import_module('users.utils.signals')

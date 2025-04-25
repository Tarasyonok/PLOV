import django.contrib.auth.backends

import users.models


class EmailAuthBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = users.models.User.objects.get(email=username)
        except users.models.User.DoesNotExist:
            try:
                user = users.models.User.objects.get(username=username)
            except users.models.User.DoesNotExist:
                return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return users.models.User.objects.get(pk=user_id)
        except users.models.User.DoesNotExist:
            return None

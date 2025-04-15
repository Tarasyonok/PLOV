import django.conf
import django.db
import django.http
import django.utils

SESSION = 300


class UserStatus(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
    )
    last_activity = django.db.models.DateTimeField()

    @staticmethod
    def update_user_activity(user):
        UserStatus.objects.update_or_create(
            user=user,
            defaults={'last_activity': django.utils.timezone.now()},
        )

    @staticmethod
    def is_user_online(user):
        try:
            user_status = UserStatus.objects.get(
                user__username=user,
            )
            online = django.utils.timezone.now() - user_status.last_activity
            if online.seconds < SESSION:
                return True

            return False
        except UserStatus.DoesNotExist:
            return django.http.Http404

    @staticmethod
    def last_seen(user):
        try:
            user_status = UserStatus.objects.get(
                user__username=user,
            )
            return user_status.last_activity
        except UserStatus.DoesNotExist:
            return django.http.Http404

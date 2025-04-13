from django.utils.deprecation import MiddlewareMixin

from users_status.models import UserStatus


class OnlineNowMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        user = request.user
        if not user.is_authenticated:
            return

        UserStatus.update_user_activity(user)

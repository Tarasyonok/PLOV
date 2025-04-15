import django.utils.deprecation

import users_status.models


class OnlineNowMiddleware(django.utils.deprecation.MiddlewareMixin):
    @staticmethod
    def process_request(request):
        user = request.user
        if not user.is_authenticated:
            return

        users_status.models.UserStatus.update_user_activity(user)

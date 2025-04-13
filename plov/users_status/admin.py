from django.contrib import admin

from users_status.models import UserStatus


class UserStatusAdmin(admin.ModelAdmin):
    list_display = (
        UserStatus.user.field.name,
        UserStatus.last_activity.field.name,
    )
    search_fields = [f'{UserStatus.user.field.name}__username',]
    list_filter = [UserStatus.last_activity.field.name]

    def get_ordering(self, request):
        return [UserStatus.last_activity.field.name]


admin.site.register(UserStatus, UserStatusAdmin)

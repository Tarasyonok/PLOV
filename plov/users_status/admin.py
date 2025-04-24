import django.contrib

import users_status.models


class UserStatusAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        users_status.models.UserStatus.user.field.name,
        users_status.models.UserStatus.last_activity.field.name,
    )
    search_fields = (f'{users_status.models.UserStatus.user.field.name}__username',)
    list_filter = (users_status.models.UserStatus.last_activity.field.name,)

    def get_ordering(self, request):
        return (users_status.models.UserStatus.last_activity.field.name,)


django.contrib.admin.site.register(users_status.models.UserStatus, UserStatusAdmin)

import django.contrib

import users_status.models


class UserStatusAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        'user',
        'last_activity',
    )
    search_fields = ('user__username',)
    list_filter = ('ulast_activity',)

    def get_ordering(self, request):
        return (users_status.models.UserStatus.last_activity.field.name,)


django.contrib.admin.site.register(users_status.models.UserStatus, UserStatusAdmin)

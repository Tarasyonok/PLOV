import django.contrib

import users_status.models


class UserStatusAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('user', 'last_activity')
    search_fields = ('user__username',)
    list_filter = ('last_activity',)

    def get_ordering(self, request):
        return ('last_activity',)


django.contrib.admin.site.register(users_status.models.UserStatus, UserStatusAdmin)

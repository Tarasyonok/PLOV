import django.contrib.admin
import django.contrib.auth.admin

import users.models


@django.contrib.admin.register(users.models.User)
class CustomUserAdmin(django.contrib.auth.admin.UserAdmin):
    @django.contrib.admin.display(description='Is LMS profile synced')
    def lms_sync_status(self, obj):
        return '❌✅'[bool(obj.lms_profile_id)]

    list_display = ('username', 'email', 'lms_sync_status', 'telegram_username', 'is_staff', 'role', 'is_banned', 'ban_reason')
    list_filter = ('is_staff', 'is_superuser')
    readonly_fields = ('lms_sync_status',)
    search_fields = ('username', 'email', 'telegram_username')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name', 'telegram_username')}),
        ('LMS Integration', {'fields': ('lms_profile_id', 'lms_sync_status')}),
        ('Permissions', {'fields': ('is_active', 'is_banned', 'ban_reason', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2'),
            },
        ),
    )


class UserProfileInline(django.contrib.admin.StackedInline):
    @django.contrib.admin.display(description='Preview')
    def avatar_preview(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" width="100" style="border-radius: 5px;" />'

        return '-'

    model = users.models.UserProfile
    fields = ('avatar_preview', 'avatar', 'bio', 'birthday', 'reputation_points')
    readonly_fields = ('avatar_preview',)


class UserCourseInline(django.contrib.admin.TabularInline):
    model = users.models.UserCourse
    extra = 0
    fields = ('specialization', 'flow_season', 'flow_year', 'is_graduated', 'rating')
    show_change_link = True


CustomUserAdmin.inlines = [UserProfileInline, UserCourseInline]


@django.contrib.admin.register(users.models.UserProfile)
class UserProfileAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('user', 'avatar_preview', 'reputation_points', 'last_activity')
    list_select_related = ('user',)
    search_fields = ('user__username', 'bio')
    readonly_fields = ('last_activity', 'avatar_preview')

    @django.contrib.admin.display(description='Avatar')
    def avatar_preview(self, obj):
        return f'<img src="{obj.avatar.url}" width="50" style="border-radius: 5px;" />' if obj.avatar else '-'


@django.contrib.admin.register(users.models.UserCourse)
class UserCourseAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('user', 'specialization_display', 'flow_year_season', 'is_graduated', 'rating')
    list_filter = ('specialization', 'flow_season', 'is_graduated')
    search_fields = ('user__username',)
    raw_id_fields = ('user',)

    @django.contrib.admin.display(description='Specialization')
    def specialization_display(self, obj):
        return obj.get_specialization_display()

    @django.contrib.admin.display(description='Flow')
    def flow_year_season(self, obj):
        return f'{obj.get_flow_season_display()} {obj.flow_year}'

    fieldsets = (
        (None, {'fields': ('user', 'specialization')}),
        ('Course Details', {'fields': ('flow_season', 'flow_year', 'is_graduated', 'rating')}),
    )

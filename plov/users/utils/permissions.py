import django.core.exceptions


def check_ownership_or_moderator(user, obj):
    if not hasattr(obj, 'user'):
        raise ValueError("Object has no 'user' attribute for ownership check")

    if not user.is_authenticated:
        raise django.core.exceptions.PermissionDenied("Login required")

    profile = user.profile
    if profile.is_moderator_or_higher():
        return True

    return obj.user == user

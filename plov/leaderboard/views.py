import django.shortcuts

import users.models


def leaderboard(request):
    user_profiles = users.models.UserProfile.objects.all()
    leaderboard = user_profiles.order_by('-reputation_points')

    return django.shortcuts.render(
        request,
        'leaderboard/leaderboard.html',
        {'leaderboard': leaderboard},
    )


def rep_leaderboard(request):
    user_profiles = users.models.UserCourse.objects.all()
    leaderboard = user_profiles.order_by('-rating')

    return django.shortcuts.render(
        request,
        'leaderboard/rep_leaderboard.html',
        {'leaderboard': leaderboard},
    )

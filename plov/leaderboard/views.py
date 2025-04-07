import django.shortcuts

import users.models


def rep_leaderboard(request):
    user_profiles = users.models.UserProfile.objects.all()
    leaderboard = user_profiles.order_by('-reputation_points')

    return django.shortcuts.render(
        request,
        'statistic/rep_leaderboard.html',
        {'leaderboard': leaderboard},
    )

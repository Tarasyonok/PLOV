import users.models


def rep_ldb_context(request):
    user_profiles = users.models.UserProfile.objects.all()
    leaderboard = user_profiles.order_by('-reputation_points')

    return {'leaderboard': leaderboard[:3]}

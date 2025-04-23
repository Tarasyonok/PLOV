import users.models


def rep_ldb_context(request):
    leader = users.models.UserProfile.objects.all().order_by('-reputation_points').first()

    return {'leader': leader}

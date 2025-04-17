import http

import django.shortcuts

import users.models


def rep_leaderboard(request):
    user_profiles = users.models.UserProfile.objects.all()
    leaderboard = user_profiles.order_by('-reputation_points')

    return django.shortcuts.render(
        request,
        'leaderboard/rep_leaderboard.html',
        {'leaderboard': leaderboard},
    )


def leaderboard(request):
    user_profiles = users.models.UserCourse.objects.all()
    leaderboard = user_profiles.order_by('-rating')

    return django.shortcuts.render(
        request,
        'leaderboard/leaderboard.html',
        {'leaderboard': leaderboard},
    )


def leaderboard_my_course(request):
    try:
        user = users.models.UserCourse.objects.filter(user=request.user).get()
        user_profiles = users.models.UserCourse.objects.filter(
            specialization=user.specialization,
            flow_season=user.flow_season,
            flow_year=user.flow_year,
        )
        leaderboard = user_profiles.order_by('-rating')

        return django.shortcuts.render(
            request,
            'leaderboard/leaderboard_my_course.html',
            {'leaderboard': leaderboard},
        )
    except users.models.UserCourse.DoesNotExist:
        return django.shortcuts.render(
            request,
            'leaderboard/leaderboard_my_course_err.html',
            status=http.HTTPStatus.NOT_FOUND,
        )

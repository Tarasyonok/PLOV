import http

import django.core.paginator
import django.shortcuts
import django.utils.timezone

import users.models


ELEMENTS_PER_PAGE = 3


def rep_leaderboard(request):
    user_profiles = users.models.UserProfile.objects.all()
    leaderboard = user_profiles.order_by('-reputation_points')

    leaderboard_indexed = []
    for i, obj in enumerate(leaderboard):
        leaderboard_indexed.append({'index': i + 1, 'object': obj})

    paginator = django.core.paginator.Paginator(leaderboard_indexed, ELEMENTS_PER_PAGE)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    return django.shortcuts.render(
        request,
        'leaderboard/rep_leaderboard.html',
        {'leaderboard': leaderboard, 'page': page},
    )


def leaderboard(request):
    user_profiles = users.models.UserCourse.objects.all()
    leaderboard = user_profiles.order_by('-rating')

    leaderboard_indexed = []
    for i, obj in enumerate(leaderboard):
        leaderboard_indexed.append({'index': i + 1, 'object': obj})

    paginator = django.core.paginator.Paginator(leaderboard_indexed, ELEMENTS_PER_PAGE)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    return django.shortcuts.render(
        request,
        'leaderboard/leaderboard.html',
        {
            'page': page,
            'year': django.utils.timezone.now().year,
            'past_year': django.utils.timezone.now().year - 1,
        },
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

        leaderboard_indexed = []
        for i, obj in enumerate(leaderboard):
            leaderboard_indexed.append({'index': i + 1, 'object': obj})

        paginator = django.core.paginator.Paginator(leaderboard_indexed, ELEMENTS_PER_PAGE)
        page_num = request.GET.get('page')
        page = paginator.get_page(page_num)

        return django.shortcuts.render(
            request,
            'leaderboard/leaderboard_my_course.html',
            {'leaderboard': leaderboard, 'page': page},
        )
    except users.models.UserCourse.DoesNotExist:
        return django.shortcuts.render(
            request,
            'leaderboard/leaderboard_my_course_err.html',
            status=http.HTTPStatus.NOT_FOUND,
        )


def leaderboard_spring(request):
    user_profiles = users.models.UserCourse.objects.filter(
        specialization='D',
        flow_season='S',
        flow_year=django.utils.timezone.now().year,
    )
    leaderboard = user_profiles.order_by('-rating')

    leaderboard_indexed = []
    for i, obj in enumerate(leaderboard):
        leaderboard_indexed.append({'index': i + 1, 'object': obj})

    paginator = django.core.paginator.Paginator(leaderboard_indexed, ELEMENTS_PER_PAGE)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    return django.shortcuts.render(
        request,
        'leaderboard/leaderboard_spring.html',
        {
            'leaderboard': leaderboard,
            'page': page,
            'year': django.utils.timezone.now().year,
            'past_year': django.utils.timezone.now().year - 1,
        },
    )


def leaderboard_spring_past(request):
    user_profiles = users.models.UserCourse.objects.filter(
        specialization='D',
        flow_season='S',
        flow_year=django.utils.timezone.now().year - 1,
    )
    leaderboard = user_profiles.order_by('-rating')

    leaderboard_indexed = []
    for i, obj in enumerate(leaderboard):
        leaderboard_indexed.append({'index': i + 1, 'object': obj})

    paginator = django.core.paginator.Paginator(leaderboard_indexed, ELEMENTS_PER_PAGE)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    return django.shortcuts.render(
        request,
        'leaderboard/leaderboard_spring_past.html',
        {
            'leaderboard': leaderboard,
            'page': page,
            'year': django.utils.timezone.now().year - 1,
            'new_year': django.utils.timezone.now().year,
        },
    )


def leaderboard_fall(request):
    user_profiles = users.models.UserCourse.objects.filter(
        specialization='D',
        flow_season='F',
        flow_year=django.utils.timezone.now().year,
    )
    leaderboard = user_profiles.order_by('-rating')

    leaderboard_indexed = []
    for i, obj in enumerate(leaderboard):
        leaderboard_indexed.append({'index': i + 1, 'object': obj})

    paginator = django.core.paginator.Paginator(leaderboard_indexed, ELEMENTS_PER_PAGE)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    return django.shortcuts.render(
        request,
        'leaderboard/leaderboard_fall.html',
        {
            'leaderboard': leaderboard,
            'page': page,
            'year': django.utils.timezone.now().year,
            'past_year': django.utils.timezone.now().year - 1,
        },
    )


def leaderboard_fall_past(request):
    user_profiles = users.models.UserCourse.objects.filter(
        specialization='D',
        flow_season='F',
        flow_year=django.utils.timezone.now().year - 1,
    )
    leaderboard = user_profiles.order_by('-rating')

    leaderboard_indexed = []
    for i, obj in enumerate(leaderboard):
        leaderboard_indexed.append({'index': i + 1, 'object': obj})

    paginator = django.core.paginator.Paginator(leaderboard_indexed, ELEMENTS_PER_PAGE)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    return django.shortcuts.render(
        request,
        'leaderboard/leaderboard_fall_past.html',
        {
            'leaderboard': leaderboard,
            'page': page,
            'year': django.utils.timezone.now().year - 1,
            'new_year': django.utils.timezone.now().year,
        },
    )

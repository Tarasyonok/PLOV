import django.urls
import leaderboard.views

app_name = 'leaderboard'

urlpatterns = [
    django.urls.path(
        'rep/',
        leaderboard.views.rep_leaderboard,
        name='rep',
    ),
    django.urls.path(
        'my/',
        leaderboard.views.leaderboard_my_course,
        name='my',
    ),
    django.urls.path(
        '',
        leaderboard.views.leaderboard,
        name='leaderboard',
    ),
]

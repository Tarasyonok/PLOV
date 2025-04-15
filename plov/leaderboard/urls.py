import django.urls
import leaderboard.views

app_name = 'leaderboards'
urlpatterns = [
    django.urls.path(
        'rep/',
        leaderboard.views.rep_leaderboard,
        name='rep',
    ),
    django.urls.path(
        '',
        leaderboard.views.leaderboard,
        name='leaderboard',
    ),
]

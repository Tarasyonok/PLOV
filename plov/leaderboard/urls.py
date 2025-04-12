import django.urls
import leaderboard.views

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

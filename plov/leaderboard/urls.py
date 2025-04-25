import django.urls

import leaderboard.views

app_name = 'leaderboard'

urlpatterns = [
    django.urls.path('rep/', leaderboard.views.rep_leaderboard, name='rep'),
    django.urls.path('my/', leaderboard.views.leaderboard_my_course, name='my'),
    django.urls.path('', leaderboard.views.leaderboard, name='leaderboard'),
    django.urls.path('spring/', leaderboard.views.leaderboard_spring, name='spring'),
    django.urls.path('spring-past/', leaderboard.views.leaderboard_spring_past, name='spring-past'),
    django.urls.path('fall/', leaderboard.views.leaderboard_fall, name='fall'),
    django.urls.path('fall-past/', leaderboard.views.leaderboard_fall_past, name='fall-past'),
]

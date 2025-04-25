import django.urls

import forum.views

app_name = 'forum'

urlpatterns = [
    django.urls.path('', forum.views.topic_list, name='forum'),
    django.urls.path('topic_post/', forum.views.topic_post, name='topic-post'),
    django.urls.path('topic/<int:pk>/', forum.views.topic_detail, name='topic-detail'),
    django.urls.path('upvote/', forum.views.upvote, name='upvote'),
    django.urls.path('downvote/', forum.views.downvote, name='downvote'),
    django.urls.path('report/topic/<int:topic_id>', forum.views.topic_report, name='topic-report'),
    django.urls.path('report/answer/<int:ans_id>', forum.views.answer_report, name='answer-report'),
]

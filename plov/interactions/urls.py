from django.urls import path

from . import views

app_name = 'interactions'

urlpatterns = [
    path('vote/review/<int:review_id>', views.vote_review, name='vote-review'),
]

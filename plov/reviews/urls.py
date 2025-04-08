import django.urls

from . import views

app_name = 'reviews'

urlpatterns = [
    django.urls.path('', views.ReviewListView.as_view(), name='reviews'),
    django.urls.path('create/', views.ReviewCreateView.as_view(), name='create'),
    django.urls.path('<int:pk>/update/', views.ReviewUpdateView.as_view(), name='update'),
    django.urls.path('<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='delete'),
]

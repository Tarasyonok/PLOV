import django.urls
import search.views

app_name = 'search'

urlpatterns = [
    django.urls.path('get_sticker_by_text/<str:text>/', search.views.SearchStickersByText.as_view(), name='getstickerbytext')
]

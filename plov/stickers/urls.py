import django.urls
import stickers.views

app_name = 'stickers'

urlpatterns = [
    django.urls.path('addstickerpack/', stickers.views.AddStickerPackView.as_view(), name='addstickerpack'),
    django.urls.path(
        'stickerpackinfo/<int:pk>/', stickers.views.StickerPackDetailView.as_view(), name='stickerpackinfo'
    ),
    django.urls.path('addsticker/<int:stickerpack_id>/', stickers.views.AddStickerView.as_view(), name='addsticker'),
]

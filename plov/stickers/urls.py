import django.urls

import stickers.views

app_name = 'stickers'

urlpatterns = [
    django.urls.path('add/stickerpack/', stickers.views.AddStickerPackView.as_view(), name='addstickerpack'),
    django.urls.path(
        'stickerpackinfo/<int:pk>/',
        stickers.views.StickerPackDetailView.as_view(),
        name='stickerpackinfo',
    ),
    django.urls.path('add/sticker/<int:stickerpack_id>/', stickers.views.AddStickerView.as_view(), name='addsticker'),
    django.urls.path('delete/sticker/<slug:pk>/<int:stickerpack_id>/', stickers.views.DeleteStickerView.as_view(), name='deletesticker'),
    django.urls.path('stickerpacks', stickers.views.StickerpackList.as_view(), name='main'),
    django.urls.path('search/sticker/', stickers.views.SearchStickerView.as_view(), name='search'),
    django.urls.path('like/sticker/<int:pk>/', stickers.views.SetLikeOnSticker.as_view(), name='like'),
]

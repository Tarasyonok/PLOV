import django.urls

import core.utils.converters
import mocklms.views

django.urls.register_converter(core.utils.converters.PositiveIntConverter, 'positive-int')

app_name = 'mocklms'

urlpatterns = [
    django.urls.path(
        '',
        mocklms.views.ProfileListView.as_view(),
        name='profile_list',
    ),
    django.urls.path(
        '<positive-int:lms_profile_id>/',
        mocklms.views.ProfileDetailView.as_view(),
        name='profile_detail',
    ),
]

import django.conf.urls.static
import django.contrib.admin
import django.urls

urlpatterns = [
    django.urls.path('users/', django.urls.include('users.urls')),
    django.urls.path('auth/', django.urls.include('django.contrib.auth.urls')),
    django.urls.path('reviews/', django.urls.include('reviews.urls')),
    django.urls.path('api/mocklms/profiles/', django.urls.include('mocklms.urls')),
    django.urls.path('admin/', django.contrib.admin.site.urls),
] + django.conf.urls.static.static(django.conf.settings.STATIC_URL, document_root=django.conf.settings.STATIC_ROOT)

if django.conf.settings.DEBUG:
    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )

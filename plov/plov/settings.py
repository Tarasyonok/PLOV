import pathlib

import decouple
import django.urls

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
SECRET_KEY = decouple.config('DJANGO_SECRET_KEY', default='FAKE-SECRET-KEY')
DEBUG = decouple.config('DJANGO_DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = decouple.config('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: v.split(','))

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_htmx',
    'core.apps.CoreConfig',
    'mocklms.apps.MocklmsConfig',
    'reviews.apps.ReviewsConfig',
    'interactions.apps.InteractionsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'plov.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'plov.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': decouple.config('POSTGRES_DB', default='plov_db'),
        'USER': decouple.config('POSTGRES_USER', default='postgres'),
        'PASSWORD': decouple.config('POSTGRES_PASSWORD', default='postgres'),
        'HOST': decouple.config('POSTGRES_HOST', default='localhost'),
        'PORT': decouple.config('POSTGRES_PORT', default='5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE
    INTERNAL_IPS = ['*']

AUTH_USER_MODEL = 'users.User'
LMS_API_URL = 'http://localhost:8000/api/mocklms'

LOGIN_URL = django.urls.reverse_lazy('users:login')
LOGIN_REDIRECT_URL = django.urls.reverse_lazy('users:profile')
LOGOUT_REDIRECT_URL = django.urls.reverse_lazy('users:login')

LOG_LEVEL = decouple.config('DJANGO_LOG_LEVEL', default='INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    },
}

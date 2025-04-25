import os

import celery
import django.conf

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plov.settings')

app = celery.Celery('plov')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

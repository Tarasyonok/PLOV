import os

import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plov.settings')

app = celery.Celery('plov')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

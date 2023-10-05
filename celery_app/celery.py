import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Web_Menu_DA.settings')

app = Celery('celery_app', include=['celery_app.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')

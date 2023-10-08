import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# celery app configuration
app.conf.CELERYBEAT_SCHEDULE = {
    'Inactivation users': {
        'task': 'tasks.inactivate_user',
        'schedule': crontab(hour='15', minute='30')
    },
}

app.conf.CELERY_TIMEZONE = 'Australia/Tasmania'

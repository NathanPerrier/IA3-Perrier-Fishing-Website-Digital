import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'


from home.celery import app as celery_app
from apps.wildlifeAPI.celery import app as wildlife_celery_app

__all__ = ('celery_app', 'wildlife_celery_app')
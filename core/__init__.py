import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'


from home.celery import app as celery_app

__all__ = ('celery_app',)
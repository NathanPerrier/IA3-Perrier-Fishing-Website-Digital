from celery import Celery
from celery.schedules import crontab
from home.celery import app as app
import logging

print(app)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **_):
    print('running 1')
    sender.add_periodic_task(crontab(minute='*/1'), clean_data.s(), name='Run every 5 minutes')
    
@app.task(bind=True)
def clean_data():
    print('running')
    from . import models as wildlife_models
    # delete all data and replace with wildlife data
    wildlife_models.WildlifeKingdoms.update()
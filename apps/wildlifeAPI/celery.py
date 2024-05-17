from celery import Celery
from celery.schedules import crontab
from home.celery import app as app
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **_):
    print(app)
    sender.add_periodic_task(5.0, clean_data.s(), name='Run every 5 minutes')

@app.task
def clean_data():
    # delete all data and replace with api data
    print("Running my task on ", app)
from celery import Celery
from celery.schedules import crontab
from home.celery import app as app
import logging

print(app)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **_):
    sender.add_periodic_task(crontab(minute='0', hour='0', day_of_month='*/2'), clean_data.s(), name='Run every 2 days')
    
@app.task(bind=True)
def clean_data():
    print('running')
    
    from . import models as wildlife_models

    wildlife_models.WildlifeKingdoms.objects.all().delete()
    wildlife_models.WildlifeClasses.objects.all().delete()
    wildlife_models.WildlifeFamilies.objects.all().delete()
    wildlife_models.WildlifeSpecies.objects.all().delete()
    wildlife_models.WildlifeSpeciesInfo.objects.all().delete()
    
    wildlife_models.WildlifeKingdoms.update(animals_only=True)
    wildlife_models.WildlifeClasses.update(animals_only=True, fish_only=True)
    wildlife_models.WildlifeFamilies.update()
    wildlife_models.WildlifeSpecies.update()
    wildlife_models.WildlifeSpeciesInfo.update()
    
if __name__ == '__main__':
    clean_data()
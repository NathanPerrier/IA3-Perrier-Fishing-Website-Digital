from django.contrib import admin
from apps.wildlifeAPI.models import *

admin.site.register(WildlifeKingdoms, )
admin.site.register(WildlifeClasses)
admin.site.register(WildlifeFamiles)
admin.site.register(WildlifeSpecies)
admin.site.register(WildlifeSpeciesInfo)

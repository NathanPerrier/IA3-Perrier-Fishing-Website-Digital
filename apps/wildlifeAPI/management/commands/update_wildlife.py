from django.core.management.base import BaseCommand, CommandError
from apps.wildlifeAPI.models import *

class Command(BaseCommand):
    help = 'Updates wildlife data'
    
    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true', help='Run in debug mode')
        parser.add_argument('--animals-only', action='store_true', help='Only add animals')
        parser.add_argument('--fish-only', action='store_true', help='Only add fish')

    def handle(self, *args, **options):
        debug = options['debug']
        animals_only = not options['animals_only']
        fish_only = options['fish_only']
        
        if not animals_only or fish_only:
            animals_only = True
            self.stdout.write(self.style.WARNING('Only adding specified fields...'))
            WildlifeKingdoms.objects.all().delete()
            WildlifeClasses.objects.all().delete()
            WildlifeFamilies.objects.all().delete()
            WildlifeSpecies.objects.all().delete()
            WildlifeSpeciesInfo.objects.all().delete()
        
        try:
            self.stdout.write(self.style.WARNING('Updating wildlife data...\nPlease Do Not Interrupt the Process!'))
            
            WildlifeKingdoms.update(debug=debug, animals_only=animals_only)
            WildlifeClasses.update(debug=debug, animals_only=animals_only)
            WildlifeFamilies.update(debug=debug)
            WildlifeSpecies.update(debug=debug, fish_only=fish_only)
            WildlifeSpeciesInfo.update(debug=debug)

            self.stdout.write(self.style.SUCCESS('Successfully updated wildlife data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to update wildlife data'))
            self.stdout.write(self.style.ERROR(e))
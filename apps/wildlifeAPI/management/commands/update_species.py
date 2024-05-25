from django.core.management.base import BaseCommand, CommandError
from apps.wildlifeAPI.models import WildlifeSpecies

class Command(BaseCommand):
    help = 'Updates wildlife species data'
    
    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true', help='Run in debug mode')
        parser.add_argument('--fish-only', action='store_true', help='Only add fish')


    def handle(self, *args, **options):
        debug = options['debug']
        fish_only = options['fish_only']
        
        if fish_only:
            self.stdout.write(self.style.WARNING('Only adding specified fields...'))
            WildlifeSpecies.objects.all().delete()
        
        try:
            self.stdout.write(self.style.WARNING('Updating wildlife species data...\nPlease Do Not Interrupt the Process!'))
            
            
            WildlifeSpecies.update(debug=debug, fish_only=fish_only)

            self.stdout.write(self.style.SUCCESS('Successfully updated wildlife species data'))
            #self.stdout.write(self.style.WARNING('Please run the following commands to update the rest of the wildlife data\n- python manage.py update_species_info'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to update wildlife species data'))
            self.stdout.write(self.style.ERROR(e))
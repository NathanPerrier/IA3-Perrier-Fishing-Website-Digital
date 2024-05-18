from django.core.management.base import BaseCommand, CommandError
from apps.wildlifeAPI.models import WildlifeSpecies

class Command(BaseCommand):
    help = 'Updates wildlife species data'
    
    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true', help='Run in debug mode')


    def handle(self, *args, **options):
        debug = options['debug']
        
        try:
            self.stdout.write(self.style.WARNING('Updating wildlife species data...\nPlease Do Not Interrupt the Process!'))
            
            WildlifeSpecies.update(debug=debug)

            self.stdout.write(self.style.SUCCESS('Successfully updated wildlife species data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to update wildlife species data'))
            self.stdout.write(self.style.ERROR(e))
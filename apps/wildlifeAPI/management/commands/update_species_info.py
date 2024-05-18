from django.core.management.base import BaseCommand, CommandError
from apps.wildlifeAPI.models import WildlifeSpeciesInfo

class Command(BaseCommand):
    help = 'Updates wildlife info data'
    
    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true', help='Run in debug mode')


    def handle(self, *args, **options):
        debug = options['debug']
        
        try:
            self.stdout.write(self.style.WARNING('Updating wildlife info data...\nPlease Do Not Interrupt the Process!'))
            
            WildlifeSpeciesInfo.update(debug=debug)

            self.stdout.write(self.style.SUCCESS('Successfully updated wildlife info data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to update wildlife info data'))
            self.stdout.write(self.style.ERROR(e))
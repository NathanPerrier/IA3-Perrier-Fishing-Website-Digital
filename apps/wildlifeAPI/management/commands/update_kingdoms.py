from django.core.management.base import BaseCommand, CommandError
from apps.wildlifeAPI.models import WildlifeKingdoms

class Command(BaseCommand):
    help = 'Updates wildlife kingdom data'
    
    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true', help='Run in debug mode')


    def handle(self, *args, **options):
        debug = options['debug']
        
        try:
            self.stdout.write(self.style.WARNING('Updating wildlife kingdom data...\nPlease Do Not Interrupt the Process!'))
            
            WildlifeKingdoms.update(debug=debug)

            self.stdout.write(self.style.SUCCESS('Successfully updated wildlife kingdom data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to update wildlife kingdom data'))
            self.stdout.write(self.style.ERROR(e))
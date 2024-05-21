from django.core.management.base import BaseCommand, CommandError
from apps.wildlifeAPI.models import WildlifeKingdoms

class Command(BaseCommand):
    help = 'Updates wildlife kingdom data'
    
    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true', help='Run in debug mode')
        parser.add_argument('--animals-only', action='store_true', help='Only add animals')

    def handle(self, *args, **options):
        debug = options['debug']
        animals_only = not options['animals_only']
        
        try:
            self.stdout.write(self.style.WARNING('Updating wildlife kingdom data...\nPlease Do Not Interrupt the Process!'))
            
            WildlifeKingdoms.update(debug=debug)

            self.stdout.write(self.style.SUCCESS('Successfully updated wildlife kingdom data'))
            self.stdout.write(self.style.WARNING('Please run the following commands to update the rest of the wildlife data:\n- python manage.py update_classes\n- python manage.py update_families\n- python manage.py update_species\n- python manage.py update_species_info'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to update wildlife kingdom data'))
            self.stdout.write(self.style.ERROR(e))
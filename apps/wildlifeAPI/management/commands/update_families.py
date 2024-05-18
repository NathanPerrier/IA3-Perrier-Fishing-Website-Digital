from django.core.management.base import BaseCommand, CommandError
from apps.wildlifeAPI.models import WildlifeFamilies

class Command(BaseCommand):
    help = 'Updates wildlife family data'
    
    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true', help='Run in debug mode')


    def handle(self, *args, **options):
        debug = options['debug']
        
        try:
            self.stdout.write(self.style.WARNING('Updating wildlife family data...\nPlease Do Not Interrupt the Process!'))
            
            WildlifeFamilies.update(debug=debug)

            self.stdout.write(self.style.SUCCESS('Successfully updated family kingdom data'))
            self.stdout.write(self.style.WARNING('Please run the following commands to update the rest of the wildlife data:\n- python manage.py update_species\n- python manage.py update_species_info'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to update wildlife family data'))
            self.stdout.write(self.style.ERROR(e))
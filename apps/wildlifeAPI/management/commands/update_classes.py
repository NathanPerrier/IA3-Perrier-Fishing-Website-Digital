from django.core.management.base import BaseCommand, CommandError
from apps.wildlifeAPI.models import WildlifeClasses

class Command(BaseCommand):
    help = 'Updates wildlife class data'
    
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
            WildlifeClasses.objects.all().delete()
        
        try:
            self.stdout.write(self.style.WARNING('Updating wildlife class data...\nPlease Do Not Interrupt the Process!'))
            
            WildlifeClasses.update(debug=debug, animals_only=animals_only, fish_only=fish_only)

            self.stdout.write(self.style.SUCCESS('Successfully updated wildlife class data'))
            #self.stdout.write(self.style.WARNING('Please run the following commands to update the rest of the wildlife data:\n- python manage.py update_families\n- python manage.py update_species\n- python manage.py update_species_info'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to update wildlife class data'))
            self.stdout.write(self.style.ERROR(e))
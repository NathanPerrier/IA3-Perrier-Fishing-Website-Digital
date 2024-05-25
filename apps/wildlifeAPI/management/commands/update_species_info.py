from django.core.management.base import BaseCommand, CommandError
from apps.wildlifeAPI.models import WildlifeSpeciesInfo, WildlifeSpeciesImage, WildlifeSpeciesConservationStatus

class Command(BaseCommand):
    help = 'Updates wildlife info data'
    
    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true', help='Run in debug mode')
        parser.add_argument('--clear', action='store_true', help='Clear Info Database')


    def handle(self, *args, **options):
        debug = options['debug']
        clear = options['clear']
        
        try:
            self.stdout.write(self.style.WARNING('Updating wildlife info data...\nPlease Do Not Interrupt the Process!'))
            
            if clear:
                WildlifeSpeciesImage.objects.all().delete()
                WildlifeSpeciesConservationStatus.objects.all().delete()
                WildlifeSpeciesInfo.objects.all().delete()
                
            WildlifeSpeciesInfo.update(debug=debug, fish_only=fish_only)

            self.stdout.write(self.style.SUCCESS('Successfully updated wildlife info data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to update wildlife info data'))
            self.stdout.write(self.style.ERROR(e))
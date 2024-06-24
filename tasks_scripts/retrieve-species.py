import os, sys
import ..apps.wildlifeAPI.models as wildlife_models

def main(argv):
        
    try:
        print('running')
        print(' EXEC FILE -> ' + os.path.basename(__file__)) 
        
        wildlife_models.WildlifeKingdoms.objects.all().delete()
        wildlife_models.WildlifeClasses.objects.all().delete()
        wildlife_models.WildlifeFamilies.objects.all().delete()
        wildlife_models.WildlifeSpecies.objects.all().delete()
        wildlife_models.WildlifeSpeciesInfo.objects.all().delete()
        
        wildlife_models.WildlifeKingdoms.update(animals_only=True)
        wildlife_models.WildlifeClasses.update(animals_only=True, fish_only=True)
        wildlife_models.WildlifeFamilies.update()
        wildlife_models.WildlifeSpecies.update()
        wildlife_models.WildlifeSpeciesInfo.update()
        
        # Unix ErrCode
        exit(0)

    except Exception as e:

        print( 'Err: ' + str( e ) )
        exit(1)

if __name__ == '__main__':
    main(sys.argv)

from django.db import models

from .wrapper import exception_handler
from .__init__ import *

class WildlifeKingdoms(models.Model):
    """Model representing a wildlife kingdom."""
    name = models.CharField(max_length=255, db_index=True)
    common_name = models.CharField(max_length=255, db_index=True)
    
    class Meta:
        verbose_name = "Wildlife Kingdom"
        verbose_name_plural = "Wildlife Kingdoms"
        
    @staticmethod
    @exception_handler
    def update(debug=False):
        WildlifeKingdoms.objects.all().delete()
        data = Kingdoms(debug=debug).get_kingdom_names()
        for kingom in data['kingdom']:
            WildlifeKingdoms(name=kingom['kingdomname'], common_name=kingom['kingdomcommonname']).save()
    
    def __str__(self):
        return self.name
    
class WildlifeClasses(models.Model):
    """Model representing a wildlife class."""
    name = models.CharField(max_length=255, db_index=True)
    common_name = models.CharField(max_length=255, db_index=True)
    kingdom = models.ForeignKey(WildlifeKingdoms, on_delete=models.CASCADE, related_name='classes')
    
    class Meta:
        verbose_name = "Wildlife Class"
        verbose_name_plural = "Wildlife Classes"
        
    @staticmethod
    @exception_handler
    def update(debug=False):
        WildlifeClasses.objects.all().delete()
        data = Classes(debug=debug).get_class_names()
        for class_ in data['class']:
            kingdom = WildlifeKingdoms.objects.filter(name=class_['kingdomname']).first()
            if kingdom is not None:
                WildlifeClasses(name=class_['classname'], common_name=class_['classcommonname'], kingdom=kingdom).save()
            else:
                print(f"No kingdom found with name {class_['kingdomname']}")
                
    def __str__(self):
        return self.name
    
class WildlifeFamilies(models.Model):
    """Model representing a wildlife family."""
    name = models.CharField(max_length=255, db_index=True)
    common_name = models.CharField(max_length=255, db_index=True)
    familyrank = models.CharField(max_length=255)
    kingdom = models.ForeignKey(WildlifeKingdoms, on_delete=models.CASCADE, related_name='families')
    class_name = models.ForeignKey(WildlifeClasses, on_delete=models.CASCADE, related_name='families')
    
    class Meta:
        verbose_name = "Wildlife Family"
        verbose_name_plural = "Wildlife Families"
        
    @staticmethod
    @exception_handler
    def update(debug=False):
        WildlifeFamilies.objects.all().delete()
        classes = WildlifeClasses.objects.all()
        for _class_ in classes:
            data = Families(debug=debug, class_=_class_.name).get_family_names()
            for family in data['family']:
                WildlifeFamilies(name=family['familyname'], common_name=family['familycommonname'], familyrank=family['familyrank'], class_name=_class_, kingdom=_class_.kingdom).save()
        
    def __str__(self):
        return self.name
    
class WildlifeSpecies(models.Model):
    """Model representing a wildlife species."""
    name = models.CharField(max_length=255, db_index=True)
    common_name = models.CharField(max_length=255, db_index=True)
    taxonid = models.CharField(max_length=255)
    endemicity = models.CharField(max_length=255)
    kingdom = models.ForeignKey(WildlifeKingdoms, on_delete=models.CASCADE, related_name='species')
    class_name = models.ForeignKey(WildlifeClasses, on_delete=models.CASCADE, related_name='species')
    family = models.ForeignKey(WildlifeFamilies, on_delete=models.CASCADE, related_name='species')
    
    @staticmethod
    @exception_handler
    def update(debug=False):
        WildlifeSpecies.objects.all().delete()
        families = WildlifeFamilies.objects.all()
        for family in families:
            data = Species(debug=debug, kingdom=family.kingdom.name, class_=family.class_name.name, family=family.name).get_species()
            for species in data['species']:
                WildlifeSpecies(name=species['scientificname'], common_name=species.get('acceptedcommonname', 'scientificname'), taxonid=species['taxonid'], endemicity=species['endemicity'], family=family, class_name=family.class_name, kingdom=family.kingdom).save()
    
    class Meta:
        verbose_name = "Wildlife Species"
        verbose_name_plural = "Wildlife Species"
    
    def __str__(self):
        return self.name

class WildlifeSpeciesInfo(models.Model):
    """Model representing a wildlife species information."""
    species = models.ForeignKey(WildlifeSpecies, on_delete=models.CASCADE, related_name='info')

    class Meta:
        verbose_name = "Wildlife Species Information"
        verbose_name_plural = "Wildlife Species Information"
        
    @staticmethod
    @exception_handler
    def update(debug=False):
        WildlifeSpeciesInfo.objects.all().delete()
        WildlifeSpeciesInfoField.objects.all().delete()
        species = WildlifeSpecies.objects.all()
        for specie in species:
            data = Species(debug=debug, taxonid=specie.taxonid, extensive_search=True, extensive_info=True).get_species_by_id()
            print(data)
            for info in data['species']:
                species_info = WildlifeSpeciesInfo(species=specie)
                species_info.save()
                if isinstance(info, list):
                    for key, value in info.items():
                        
                        WildlifeSpeciesInfoField(info=species_info, name=key, value=value).save()
                else: WildlifeSpeciesInfoField(info=species_info, name=info, value=data[info]).save()

    def __str__(self):
        return self.species.name

class WildlifeSpeciesInfoField(models.Model):
    """Model representing a dynamic field for a wildlife species information."""
    info = models.ForeignKey(WildlifeSpeciesInfo, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        verbose_name = "Wildlife Species Information Field"
        verbose_name_plural = "Wildlife Species Information Fields"

    def __str__(self):
        return f"{self.name}: {self.value}"
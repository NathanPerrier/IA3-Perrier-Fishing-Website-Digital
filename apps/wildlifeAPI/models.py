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
    def update(debug=False, animals_only=False):
        data = Kingdoms(debug=debug, exclude_kingdom=animals_only).get_kingdom_names()
        for kingom in data['kingdom']:
            WildlifeKingdoms.objects.update_or_create(name=kingom['kingdomname'], common_name=kingom['kingdomcommonname'])
    
    def __str__(self):
        return self.name
    
class WildlifeClasses(models.Model):
    """Model representing a wildlife class."""
    name = models.CharField(max_length=255, db_index=True)
    common_name = models.CharField(max_length=255, db_index=True)
    kingdom = models.ForeignKey(WildlifeKingdoms, on_delete=models.CASCADE, related_name='classes')
    kingdom_name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Wildlife Class"
        verbose_name_plural = "Wildlife Classes"
        
    @staticmethod
    @exception_handler
    def update(debug=False, animals_only=False):
        kingdoms = WildlifeKingdoms.objects.all() if animals_only else WildlifeKingdoms.objects.filter(common_name='animals')
        for kingdom in kingdoms:
            data = Classes(debug=debug, kingdom=kingdom.common_name).get_class_names()  # for each kingdom
            for class_ in data['class']:
                kingdom = WildlifeKingdoms.objects.filter(name=class_['kingdomname']).first()
                if kingdom is not None: WildlifeClasses.objects.update_or_create(name=class_['classname'], common_name=class_['classcommonname'], kingdom=kingdom, kingdom_name=kingdom.name)
                else: print(f"No kingdom found with name {class_['kingdomname']}")
                
    def __str__(self):
        return self.name
    
class WildlifeFamilies(models.Model):
    """Model representing a wildlife family."""
    name = models.CharField(max_length=255, db_index=True)
    common_name = models.CharField(max_length=255, db_index=True)
    familyrank = models.CharField(max_length=255)
    kingdom = models.ForeignKey(WildlifeKingdoms, on_delete=models.CASCADE, related_name='families')
    kingdom_name = models.CharField(max_length=255)
    _class = models.ForeignKey(WildlifeClasses, on_delete=models.CASCADE, related_name='families')
    class_name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Wildlife Family"
        verbose_name_plural = "Wildlife Families"
        
    @staticmethod
    @exception_handler
    def update(debug=False):
        classes = WildlifeClasses.objects.all()
        for _class_ in classes:
            data = Families(debug=debug, class_=_class_.name, kingdom=_class_.kingdom.common_name).get_family_names()
            for family in data['family']:
                WildlifeFamilies.objects.update_or_create(name=family['familyname'], common_name=family['familycommonname'], familyrank=family['familyrank'], _class=_class_, class_name=_class_.name, kingdom=_class_.kingdom, kingdom_name=_class_.kingdom.name)
        
    def __str__(self):
        return self.name
    
class WildlifeSpecies(models.Model):
    """Model representing a wildlife species."""
    name = models.CharField(max_length=255, db_index=True)
    common_name = models.CharField(max_length=255, db_index=True)
    taxonid = models.CharField(max_length=255)
    kingdom = models.ForeignKey(WildlifeKingdoms, on_delete=models.CASCADE, related_name='species')
    kingdom_name = models.CharField(max_length=255)
    _class = models.ForeignKey(WildlifeClasses, on_delete=models.CASCADE, related_name='species')
    class_name = models.CharField(max_length=255)
    family = models.ForeignKey(WildlifeFamilies, on_delete=models.CASCADE, related_name='species')
    family_name = models.CharField(max_length=255)
    
    @staticmethod
    @exception_handler
    def update(debug=False):
        families = WildlifeFamilies.objects.all()
        for family in families:
            data = Species(debug=debug, kingdom=family.kingdom.name, class_=family._class.name, family=family.name).get_species()
            for species in data['species']:
                WildlifeSpecies.objects.update_or_create(name=species['scientificname'], common_name=species.get('acceptedcommonname', species['scientificname']), taxonid=species['taxonid'], family=family, family_name=family.name, _class=family._class, class_name=family._class.name, kingdom=family.kingdom, kingdom_name=family.kingdom.name)
    
    class Meta:
        verbose_name = "Wildlife Species"
        verbose_name_plural = "Wildlife Species"
    
    def __str__(self):
        return self.name
    
class WildlifeSpeciesConservationStatus(models.Model):
    species = models.OneToOneField(WildlifeSpecies, on_delete=models.CASCADE, related_name='conservation_status')
    species_name = models.CharField(max_length=255)
    nca_status = models.CharField(max_length=255, null=True)
    nca_status_code = models.CharField(max_length=1, null=True)
    conservation_significant = models.BooleanField(null=True)
    
    def __str__(self):
        return self.species.name

class WildlifeSpeciesImage(models.Model):
    species = models.ForeignKey(WildlifeSpecies, on_delete=models.CASCADE, related_name='image')
    species_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True)
    format = models.CharField(max_length=255, null=True)
    url = models.URLField(null=True)
    reference = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    
    @staticmethod
    def add_images(specie, data):
        if 'image' in data:
            if isinstance(data['image'], dict):     
                WildlifeSpeciesImage.objects.update_or_create(species=specie, species_name=specie.name, type=data['image']['type'], format=data['image']['format'], url=data['image']['url'], reference=data['image']['reference'], title=data['image']['title'])
            else:
                for image in data['image']:
                    WildlifeSpeciesImage.objects.update_or_create(species=specie, species_name=specie.name, type=image['type'], format=image['format'], url=image['url'], reference=image['reference'], title=image['title'])
        
    
    def __str__(self):
        return self.species.name
    

class WildlifeSpeciesInfo(models.Model):
    """Model representing a wildlife species information."""
    species = models.ForeignKey(WildlifeSpecies, on_delete=models.CASCADE, related_name='info')
    species_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    endemicity = models.CharField(max_length=255)
    wetland_status = models.CharField(max_length=255, null=True, blank=True)
    synonyms = models.CharField(max_length=255, null=True, blank=True)
    pest_status = models.CharField(max_length=255)
    environment = models.CharField(max_length=255, null=True, blank=True)
    conservation_status = models.OneToOneField(WildlifeSpeciesConservationStatus, on_delete=models.CASCADE, related_name='info', null=True, blank=True)
    isSuperseded = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Wildlife Species Information"
        verbose_name_plural = "Wildlife Species Information"
        
    @staticmethod
    @exception_handler
    def update(debug=False):
        species = WildlifeSpecies.objects.all()
        
        for specie in species:
            data = Species(debug=debug, kingdom=specie.kingdom.name, taxonid=specie.taxonid).get_species_by_id() # i removed extensive_search
            WildlifeSpeciesInfo.add_info(specie, data['species'])
        
    @staticmethod
    def add_info(specie, data):
        conservation=None

        WildlifeSpeciesImage.add_images(specie, data)
        
        if 'conservationstatus' in data:
            conservation, created = WildlifeSpeciesConservationStatus.objects.update_or_create(species=specie, species_name=specie.name, nca_status=data['conservationstatus'].get('ncastatus', 'Not Evaluated'), nca_status_code=data['conservationstatus'].get('ncastatuscode', 'Not Evaluated'), conservation_significant=data['conservationstatus'].get('conservationsignificant', False))
            
        WildlifeSpeciesInfo.objects.update_or_create(
            species=specie,
            species_name=specie.name,
            description=data['profile'].get('description', None),
            endemicity=data.get('endemicity', 'Not Evaluated'),
            wetland_status=data.get('wetlandstatus', 'N/A'),
            synonyms=data.get('synonyms', None),
            pest_status=data.get('peststatus', None),
            environment=data.get('speciesenvironment', None),
            isSuperseded=data.get('isSuperseded', False),
            conservation_status=conservation,
        )

    def __str__(self):
        return self.species.name



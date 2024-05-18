from django.db import models
from .__init__ import *

class WildlifeKingdoms(models.Model):
    """Model representing a wildlife kingdom."""
    name = models.CharField(max_length=255, db_index=True)
    common_name = models.CharField(max_length=255, db_index=True)
    
    class Meta:
        verbose_name = "Wildlife Kingdom"
        verbose_name_plural = "Wildlife Kingdoms"
        
    @staticmethod
    def update():
        # update all data
        data = Kingdoms().get_kingdom_names()
        print(data)
    
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
    
    def __str__(self):
        return self.name
    
class WildlifeFamiles(models.Model):
    """Model representing a wildlife family."""
    name = models.CharField(max_length=255, db_index=True)
    common_name = models.CharField(max_length=255, db_index=True)
    familyrank = models.CharField(max_length=255)
    kingdom = models.ForeignKey(WildlifeKingdoms, on_delete=models.CASCADE, related_name='families')
    class_name = models.ForeignKey(WildlifeClasses, on_delete=models.CASCADE, related_name='families')
    
    class Meta:
        verbose_name = "Wildlife Family"
        verbose_name_plural = "Wildlife Families"
    
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
    family = models.ForeignKey(WildlifeFamiles, on_delete=models.CASCADE, related_name='species')
    
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
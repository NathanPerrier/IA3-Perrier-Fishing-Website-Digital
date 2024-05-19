from rest_framework import serializers
from apps.common.models import Product
from django.contrib.auth.models import User
from ..wildlifeAPI.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class WildlifeKingdomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WildlifeKingdoms
        fields = '__all__'
    
class WildlifeClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WildlifeClasses
        fields = '__all__'

class WildlifeFamiliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WildlifeFamilies
        fields = '__all__'
        
class WildlifeSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WildlifeSpecies
        fields = '__all__'
        

class WildlifeSpeciesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WildlifeSpeciesInfo
        fields = '__all__'

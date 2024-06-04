from rest_framework import serializers
from django.contrib.auth.models import User
from apps.users.models import *
from apps.wildlifeAPI.models import *
from apps.social.models import *

class FollowersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Followers
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    following = FollowersSerializer(Profile, many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ['password']
        
        
# class SocialPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         models = Post
#         fields = '__all__'
        

        
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

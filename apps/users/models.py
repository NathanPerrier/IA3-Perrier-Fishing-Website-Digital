from django.db import models
from django.contrib.auth.models import User

# Create your models here.


ROLE_CHOICES = (
    ('admin'  , 'Admin'),
    ('user'  , 'User'),
)
class Profile(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE)
    role      = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    full_name = models.CharField(max_length=255, null=True, blank=True)
    country   = models.CharField(max_length=255, null=True, blank=True)
    city      = models.CharField(max_length=255, null=True, blank=True)
    zip_code  = models.CharField(max_length=255, null=True, blank=True)
    address   = models.CharField(max_length=255, null=True, blank=True)
    phone     = models.CharField(max_length=255, null=True, blank=True)
    avatar    = models.ImageField(upload_to='avatar', null=True, blank=True)
    bio      = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Followers(models.Model):
    """ followers and following """
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_from_profile')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_to_profile')
        
    def get_followers_by_profile(self, user_profile):
        return self.objects.filter(following=user_profile)

    def get_following_by_profile(self, user_profile):
        return self.objects.filter(follower=user_profile)
    
    def is_following(self, user_profile):
        return self.__class__.objects.filter(follower=self.follower, following=user_profile).exists()
    
    def follow(self):
        if self.is_following(self.following):
            return None
    
        if self.following == self.follower:
            print('You cannot follow yourself')
            return None
    
        return self.__class__.objects.update_or_create(follower=self.follower, following=self.following)
    
    def unfollow(self):
        return self.__class__.objects.filter(follower=self.follower, following=self.following).delete()
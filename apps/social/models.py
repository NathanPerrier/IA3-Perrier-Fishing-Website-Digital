# post, rating, social (followers), following, likes, comments), notification, message, report, abuse, block, mute, tag, share, comment
from django.db import models
from apps.users.models import Profile
from apps.wildlifeAPI.models import WildlifeSpecies

class Post(models.Model):
    """ post model """
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post', null=True, blank=True)
    species = models.ForeignKey(WildlifeSpecies, on_delete=models.PROTECT, null=True, blank=True)
    
    def __str__(self):
        return self.content
    
    def get_user_posts(self, user):
        return self.objects.filter(user_profile=user)
    
    def get_post(self, post_id):
        return self.objects.get(id=post_id)
    
    def get_species_posts(self, species):
        return self.objects.filter(species=species)
    
    def get_posts_by_species_name(self, species_name):
        return self.objects.filter(species__name=species_name)
    
    def get_posts_by_rating(self):
        return self.objects.order_by('-rating')
    
class Followers(models.Model):
    """ followers and following """
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_from_profile')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_to_profile')
    
    def __str__(self):
        return f'{self.follower} follows {self.following}'
    
        
    def get_followers_by_profile(self, user_profile):
        return self.objects.filter(following=user_profile)

    def get_following_by_profile(self, user_profile):
        return self.objects.filter(follower=user_profile)

class Rating(models.Model):
    """ likes or dislikes on a post """
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.IntegerField()
    
    def __str__(self):
        return f'{self.user_profile} rated {self.post}'
    
    def get_likes(self, post):
        return self.objects.filter(post=post, rating=-1)
    
    def get_post_dislikes(self, post):
        return self.objects.filter(post=post, rating=-1)
    
class Comment(models.Model):
    """ nested comments """
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    relates_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.content
    
    def get_post_comments(self, post):
        return self.objects.filter(post=post)
    
    def get_comment_replies(self, comment):
        return self.objects.filter(relates_to=comment)
    
class CommentRating(models.Model):
    """ likes or dislikes on a comment """
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    rating = models.IntegerField()
    
    def __str__(self):
        return f'{self.user_profile} rated {self.comment}'
    
    def get_comment_likes(self, comment):
        return self.objects.filter(comment=comment, rating=-1)
    
    def get_comment_dislikes(self, comment):
        return self.objects.filter(comment=comment, rating=-1)
    
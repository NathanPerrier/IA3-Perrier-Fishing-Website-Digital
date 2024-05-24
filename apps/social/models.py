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
    species = models.ForeignKey(WildlifeSpecies, on_delete=models.PROTECT, null=True, blank=True)
    
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
    
class PostImages(models.Model):
    """ post images """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images/')
    
    def get_post_images(self, post):
        return self.objects.filter(post=post)
    
    def get_post_image(self, post, image_id):
        return self.objects.get(post=post, id=image_id)

class Rating(models.Model):
    """ likes or dislikes on a post """
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.IntegerField()
    
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
    
    def get_post_comments(self, post):
        return self.objects.filter(post=post)
    
    def get_comment_replies(self, comment):
        return self.objects.filter(relates_to=comment)
    
class CommentRating(models.Model):
    """ likes or dislikes on a comment """
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    rating = models.IntegerField()
    
    def get_comment_likes(self, comment):
        return self.objects.filter(comment=comment, rating=-1)
    
    def get_comment_dislikes(self, comment):
        return self.objects.filter(comment=comment, rating=-1)
    
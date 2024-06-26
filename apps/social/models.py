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

class PostLikes(models.Model):
    """ likes on a post """
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def get_post_likes(self, post):
        return self.objects.filter(post=post)
    
    
class PostSaved(models.Model):
    """ saved posts """
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
        
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
    
class CommentLikes(models.Model):
    """ likes or dislikes on a comment """
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    
    def get_comment_likes(self, comment):
        return self.objects.filter(comment=comment)
    
    
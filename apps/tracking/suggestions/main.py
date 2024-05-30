from apps.tracking.suggestions.__init__ import *
from django.db.models import Count
from django.db.models.functions import ExtractHour


class Suggestions:
    def __init__(self, user):
        """ Initialize the Suggestions class with the user's profile. """
        
        self.user = user

        # Top Profiles
        self.top_profiles_urls = (
            Routes.objects.filter(user=user, current_url__icontains='/profile/')
            .values('current_url')
            .annotate(visit_count=Count('current_url'))
            .order_by('-visit_count')
        )
        
        self.top_profile_usernames = [
            url['current_url'].split('/') for url in self.top_profiles_urls
        ]
        
        for i, endpoints in enumerate(self.top_profile_usernames):
            for username in endpoints:
                if username in Profile.objects.values_list('user__username', flat=True):
                    if username != user.username:
                        self.top_profile_usernames[i] = username
                  
        self.top_profiles = Profile.objects.filter(user__username__in=self.top_profile_usernames)

        self.top_profile_posts = Post.objects.filter(user_profile__in=self.top_profiles)

        # Likes
        self.liked_posts = (
            PostLikes.objects.filter(user_profile=self.user.profile)
            .values_list('post', flat=True)
        )

        # Saves
        self.saved_posts = (
            PostSaved.objects.filter(user_profile=self.user.profile)
            .values_list('post', flat=True)
        )

        # Follows
        self.followed_profiles = Followers.objects.filter(follower=self.user.profile).values_list('following', flat=True)
        self.followed_posts = Post.objects.filter(user_profile__in=self.followed_profiles)

    def suggest_posts(self):
        """ Suggest posts based on the user's activity. """
        all_posts = (
            self.top_profile_posts
            | Post.objects.filter(id__in=self.liked_posts)
            | Post.objects.filter(id__in=self.saved_posts)
            | self.followed_posts
        )

        top_posts = (
            all_posts.annotate(like_count=Count('postlikes'), save_count=Count('postsaved'))
            .order_by('-like_count', '-save_count')
        )

        return top_posts.order_by('-created_at')

    def suggest_other_profiles(self):
        """ Suggest other profiles based on the user's activity. """
        return self.top_profiles[:5]
    
    
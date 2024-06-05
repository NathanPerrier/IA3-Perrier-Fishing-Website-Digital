from apps.social.models import *
from apps.users.models import Profile, Followers
from django.db.models import Count
from django.contrib.auth.models import User
from collections import defaultdict

def profile_filter(request):
    filter_string = {}
    filter_mappings = {
        'search': 'user__username__icontains'
    }
    for key in request.GET:
        if request.GET.get(key) and key != 'page':
            filter_string[filter_mappings[key]] = request.GET.get(key)

    return filter_string

def get_top_posts():
    """ get top posts by number of likes, comments, and saves """
    posts = Post.objects.annotate(
        total_likes=Count('postlikes'),
        total_comments=Count('comment'),
        total_saves=Count('postsaved')
    ).order_by('-total_likes', '-total_comments', '-total_saves')
    
    for post in posts:
        post.total_likes = PostLikes.objects.filter(post=post).count()
        post.total_comments = Comment.objects.filter(post=post).count()
        post.total_saves = PostSaved.objects.filter(post=post).count()
        post.images = PostImages.objects.filter(post=post).all()
    
    return posts

def get_top_profiles():
    """ get top profiles by number of followers """
    profiles = Profile.objects.annotate(
        total_followers=Count('user_to_profile')
    ).order_by('-total_followers')
    
    for profile in profiles:
        profile.total_followers = Followers.objects.filter(following=profile).count()
    
    return profiles

def sort_posts_by_week():
    """ get posts sorted by week """
    posts = Post.objects.all()
    posts = sorted(posts, key=lambda x: x.created_at.isocalendar()[1], reverse=True)
    return posts

def sort_users_by_day():
    """ get users sorted by day """
    users = User.objects.all()
    users_by_day = {i: [] for i in range(7)}  # Initialize with empty lists for each day

    for user in users:
        day_of_week = user.date_joined.weekday()  # Monday is 0 and Sunday is 6
        users_by_day[day_of_week].append(user)
    
    # Change to store the number of users instead of the users themselves
    sorted_users_by_day = [len(users) for day, users in sorted(users_by_day.items())]
    print(sorted_users_by_day)
    return sorted_users_by_day

def sort_posts_by_day():
    """ get posts sorted by day """
    posts = Post.objects.all()
    posts = sorted(posts, key=lambda x: x.created_at.isocalendar()[2], reverse=True)
    return posts
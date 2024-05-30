from apps.social.models import Post, PostImages, PostLikes, PostSaved, Comment, CommentLikes
from .models import Followers
from apps.wildlifeAPI.models import *

def user_filter(request):
    filter_string = {}
    filter_mappings = {
        'search': 'username__icontains'
    }
    for key in request.GET:
        if request.GET.get(key) and key != 'page':
            filter_string[filter_mappings[key]] = request.GET.get(key)

    return filter_string


def get_profile_posts(request, profile):
    posts = Post.objects.filter(user_profile=profile).order_by('-created_at')

    # Get additional data for each post
    for post in posts:
        post.likes = PostLikes.objects.filter(post=post)
        post.images = PostImages.objects.filter(post=post)
        post.comments = Comment.objects.filter(post=post)
        if request.user.is_authenticated:
            post.liked = PostLikes.objects.filter(post=post, user_profile=request.user.profile).exists()
            post.saved = PostSaved.objects.filter(post=post, user_profile=request.user.profile).exists()
        for comment in post.comments:
            comment.likes = CommentLikes.objects.filter(comment=comment)
            comment.comments = Comment.objects.filter(relates_to=comment)
            if request.user.is_authenticated: comment.liked = CommentLikes.objects.filter(comment=comment, user_profile=request.user.profile).exists()
            for sub_comment in comment.comments:
                sub_comment.likes = CommentLikes.objects.filter(comment=sub_comment)
                if request.user.is_authenticated: sub_comment.liked = CommentLikes.objects.filter(comment=sub_comment, user_profile=request.user.profile).exists()

    return posts

def get_saved_posts(request, profile):
    posts = PostSaved.objects.filter(user_profile=profile).all()

    posts = [post.post for post in posts]

    # Get additional data for each post
    for post in posts:
        post.likes = PostLikes.objects.filter(post=post)
        post.images = PostImages.objects.filter(post=post)
        post.comments = Comment.objects.filter(post=post)
        if request.user.is_authenticated:
            post.liked = PostLikes.objects.filter(post=post, user_profile=request.user.profile).exists()
            post.saved = PostSaved.objects.filter(post=post, user_profile=request.user.profile).exists()
        for comment in post.comments:
            comment.likes = CommentLikes.objects.filter(comment=comment)
            comment.comments = Comment.objects.filter(relates_to=comment)
            if request.user.is_authenticated: comment.liked = CommentLikes.objects.filter(comment=comment, user_profile=request.user.profile).exists()
            for sub_comment in comment.comments:
                sub_comment.likes = CommentLikes.objects.filter(comment=sub_comment)
                if request.user.is_authenticated: sub_comment.liked = CommentLikes.objects.filter(comment=sub_comment, user_profile=request.user.profile).exists()

    return posts

def get_followers_posts(request, profile):
    followers = Followers.objects.filter(following=profile).all()
    posts = []
    for follower in followers:
        posts += Post.objects.filter(user_profile=follower.follower).order_by('-created_at')

    # Get additional data for each post
    for post in posts:
        post.likes = PostLikes.objects.filter(post=post)
        post.images = PostImages.objects.filter(post=post)
        post.comments = Comment.objects.filter(post=post)
        if request.user.is_authenticated:
            post.liked = PostLikes.objects.filter(post=post, user_profile=request.user.profile).exists()
            post.saved = PostSaved.objects.filter(post=post, user_profile=request.user.profile).exists()
        for comment in post.comments:
            comment.likes = CommentLikes.objects.filter(comment=comment)
            comment.comments = Comment.objects.filter(relates_to=comment)
            if request.user.is_authenticated: comment.liked = CommentLikes.objects.filter(comment=comment, user_profile=request.user.profile).exists()
            for sub_comment in comment.comments:
                sub_comment.likes = CommentLikes.objects.filter(comment=sub_comment)
                if request.user.is_authenticated: sub_comment.liked = CommentLikes.objects.filter(comment=sub_comment, user_profile=request.user.profile).exists()

    return posts

def get_following_posts(request, profile):
    following = Followers.objects.filter(follower=profile).all()
    posts = []
    for follow in following:
        posts += Post.objects.filter(user_profile=follow.following).order_by('-created_at')

    # Get additional data for each post
    for post in posts:
        post.likes = PostLikes.objects.filter(post=post)
        post.images = PostImages.objects.filter(post=post)
        post.comments = Comment.objects.filter(post=post)
        if request.user.is_authenticated:
            post.liked = PostLikes.objects.filter(post=post, user_profile=request.user.profile).exists()
            post.saved = PostSaved.objects.filter(post=post, user_profile=request.user.profile).exists()
        for comment in post.comments:
            comment.likes = CommentLikes.objects.filter(comment=comment)
            comment.comments = Comment.objects.filter(relates_to=comment)
            if request.user.is_authenticated: comment.liked = CommentLikes.objects.filter(comment=comment, user_profile=request.user.profile).exists()
            for sub_comment in comment.comments:
                sub_comment.likes = CommentLikes.objects.filter(comment=sub_comment)
                if request.user.is_authenticated: sub_comment.liked = CommentLikes.objects.filter(comment=sub_comment, user_profile=request.user.profile).exists()

    return posts
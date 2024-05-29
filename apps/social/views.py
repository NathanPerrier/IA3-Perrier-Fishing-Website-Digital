from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from apps.users.models import Profile

from .models import Post, PostImages, PostLikes, PostSaved, Comment, CommentLikes
from apps.wildlifeAPI.models import *
from .utils import get_image_urls
from .wrapper import group_required

def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    # Get additional data for each post
    for post in posts:
        post.likes = PostLikes.objects.filter(post=post)
        post.images = PostImages.objects.filter(post=post)
        post.comments = Comment.objects.filter(post=post)
        post.liked = PostLikes.objects.filter(post=post, user_profile=request.user.profile).exists()
        post.saved = PostSaved.objects.filter(post=post, user_profile=request.user.profile).exists()
        for comment in post.comments:
            comment.likes = CommentLikes.objects.filter(comment=comment)
            comment.comments = Comment.objects.filter(relates_to=comment)
            comment.liked = CommentLikes.objects.filter(comment=comment, user_profile=request.user.profile).exists()
            for sub_comment in comment.comments:
                sub_comment.likes = CommentLikes.objects.filter(comment=sub_comment)
                sub_comment.liked = CommentLikes.objects.filter(comment=sub_comment, user_profile=request.user.profile).exists()

    fish = WildlifeSpecies.objects.all()

    return render(request, 'pages/social/feed.html', {'posts': posts, 'fishes': fish})

@group_required('member', 'leader', 'staff', 'admin')
def create_post(request):
    if request.method == 'POST':
        try:
            file_urls = get_image_urls(request)
            content = request.POST['content']
            
            species = WildlifeSpecies.objects.filter(common_name=request.POST['species']).first()
            
            if not species and request.POST['species']:
                species = WildlifeSpecies.objects.filter(common_name__icontains=request.POST['species']).first()
            
            post = Post.objects.create(
                user_profile=request.user.profile,
                content=content,
                species=species
            )
            
            if file_urls:
                try:
                    for url in file_urls:
                        PostImages.objects.create(
                            post=post,
                            image=url
                        )
                except Exception as e:
                    messages.error(request, 'There was an error uploading your images. Please try again later.')
                    print(e)

            return JsonResponse({'success': True})
        
        except Exception as e:
            messages.error(request, 'There was an error creating your post. Please try again later.')
            print(e)

    return render(request, 'pages/social/create_post.html', {'species': WildlifeSpecies.objects.all()})


@group_required('member', 'leader', 'staff', 'admin')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user_profile.user == request.user or (request.user.is_staff or request.user.is_superuser):
        if request.method == 'POST':
            try:
                post.content = request.POST['content']
                post.save()
                messages.success(request, 'Post updated successfully.')
                return redirect('/') 
            
            except Exception as e:
                messages.error(request, 'There was an error updating your post. Please try again later.')
                print(e)
    else:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('/')
    
    return render(request, 'pages/social/edit_post.html', {'post': post, 'species': WildlifeSpecies.objects.all()})


 #? should non club memebers be able to comment?
@login_required(login_url='/users/signin/')
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        print(request.POST)
        try:
            content = request.POST['content']
            print(content)
            Comment.objects.create(
                user_profile=request.user.profile,
                post=post,
                content=content
            )
            messages.success(request, 'Comment created successfully.')
            return redirect('/social/feed/')
        except Exception as e:
            messages.error(request, 'There was an error creating your comment. Please try again later.')
            print(e)
    return redirect('/social/feed/')

@login_required(login_url='/users/signin/')
def create_nested_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        try:
            content = request.POST['content']
            Comment.objects.create(
                user_profile=request.user.profile,
                post=comment.post,
                content=content,
                relates_to=comment
            )
            messages.success(request, 'Comment created successfully.')
            return redirect('/social/feed/')
        except Exception as e:
            messages.error(request, 'There was an error creating your comment. Please try again later.')
            print(e)
    return redirect('/social/feed/')
        
@login_required(login_url='/users/signin/')    
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = PostLikes.objects.filter(post=post, user_profile=request.user.profile).first()
    
    if like:
        like.delete()
    else:
        PostLikes.objects.create(
            post=post,
            user_profile=request.user.profile
        )
    
    return redirect('/social/feed/')

@login_required(login_url='/users/signin/')
def like_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like = CommentLikes.objects.filter(comment=comment, user_profile=request.user.profile).first()
    
    if like:
        like.delete()
    else:
        CommentLikes.objects.create(
            comment=comment,
            user_profile=request.user.profile
        )
    
    return redirect('/social/feed/')

@login_required(login_url='/users/signin/')
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    save = PostSaved.objects.filter(post=post, user_profile=request.user.profile).first()
    
    if save:
        save.delete()
    else:
        PostSaved.objects.create(
            post=post,
            user_profile=request.user.profile
        )
    
    return redirect('/social/feed/')

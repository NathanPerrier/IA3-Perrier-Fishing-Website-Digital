from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from apps.users.models import Profile, Followers

from .models import Post, PostImages, PostLikes, PostSaved, Comment, CommentLikes
from apps.wildlifeAPI.models import *
from .utils import get_image_urls, post_filter
from .wrapper import *
from .forms import PostAdminForm
from django.conf import settings


def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    request.session.pop('file_urls', None)

    # Get additional data for each post
    for post in posts:
        post.likes = PostLikes.objects.filter(post=post)
        post.images = PostImages.objects.filter(post=post)
        post.comments = Comment.objects.filter(post=post)
        if request.user.is_authenticated:
            post.is_following = Followers.objects.filter(follower=request.user.profile, following=post.user_profile).exists()
            post.liked = PostLikes.objects.filter(post=post, user_profile=request.user.profile).exists()
            post.saved = PostSaved.objects.filter(post=post, user_profile=request.user.profile).exists()
        for comment in post.comments:
            comment.likes = CommentLikes.objects.filter(comment=comment)
            comment.comments = Comment.objects.filter(relates_to=comment)
            if request.user.is_authenticated: comment.liked = CommentLikes.objects.filter(comment=comment, user_profile=request.user.profile).exists()
            for sub_comment in comment.comments:
                sub_comment.likes = CommentLikes.objects.filter(comment=sub_comment)
                if request.user.is_authenticated: sub_comment.liked = CommentLikes.objects.filter(comment=sub_comment, user_profile=request.user.profile).exists()

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
                file_urls = get_image_urls(request)
                post.content = request.POST['content']
                
                species = WildlifeSpecies.objects.filter(common_name=request.POST['species']).first()
                
                if not species and request.POST['species']:
                    species = WildlifeSpecies.objects.filter(common_name__icontains=request.POST['species']).first()
                
                post.species = species
                
                post.save()
                
                if file_urls:
                    PostImages.objects.delete(post=post)
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
                messages.error(request, 'There was an error updating your post. Please try again later.')
                print(e)
    else:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('/social/feed/')
    
    return render(request, 'pages/social/edit_post.html', {'post': post, 'species': WildlifeSpecies.objects.all(), 'media_root': settings.MEDIA_URL})


 #? should non club memebers be able to comment?
@extended_group_required('member', 'leader', 'staff', 'admin')
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

@extended_group_required('member', 'leader', 'staff', 'admin')
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

@admin_required
def datatables(request):
  filters = post_filter(request)
  product_list = Post.objects.filter(**filters)
  form = PostAdminForm()

  page = request.GET.get('page', 1)
  paginator = Paginator(product_list, 5)
  posts = paginator.page(page)

  if request.method == 'POST':
      form = PostAdminForm(request.POST)
      if form.is_valid():
          return post_request_handling(request, form)

  context = {
    'segment'  : 'social',
    'parent'   : 'apps',
    'form'     : form,
    'posts' : posts
  }
  
  return render(request, 'apps/social.html', context)


@admin_required
def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@admin_required
def update_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        post.name = request.POST.get('name')
        post.price = int(request.POST.get('price'))
        post.info = request.POST.get('info')
        post.save()
    return redirect(request.META.get('HTTP_REFERER'))
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from apps.users.models import Profile
import json

from .models import Post, PostImages, PostLikes, PostSaved, Comment, CommentLikes
from apps.wildlifeAPI.models import *
from .utils import get_image_urls

def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    #fish = Species(species="fish").species_search()
    fish = WildlifeSpecies.objects.all()

    return render(request, 'pages/social/feed.html', {'posts': posts, 'fishes': fish})

@login_required(login_url='/users/signin')
def create_post(request):
    if request.method == 'POST':
        try:
            file_urls = get_image_urls(request)
            content = request.POST['content']
            
            species = WildlifeSpecies.objects.filter(common_name=request.POST['species']).first()
            
            if not species and request.POST['species']:
                species = WildlifeSpecies.objects.filter(common_name__icontains=request.POST['species']).first()
            
            Post.objects.create(
                user_profile=request.user.profile,
                content=content,
                species=species
            )
            
            for url in file_urls:
                PostImages.objects.create(
                    post=Post.objects.last(),
                    image=url
                )

            return redirect('/') 
        
        except Exception as e:
            messages.error(request, 'There was an error creating your post. Please try again later.')
            print(e)

    return render(request, 'pages/social/create_post.html', {'species': WildlifeSpecies.objects.all()})

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
        
        file_urls = get_image_urls(request)
        content = json.loads(request.POST['content'])
        
        try:
            species = WildlifeSpecies.objects.get(common_name=request.POST['species'])
        except:
            species = None
            
        print(species)
        
        if not species and request.POST['species']:
            species = WildlifeSpecies.objects.filter(common_name__icontains=request.POST['species']).first()
        
        print(content)
        print(file_urls)

    return render(request, 'pages/social/create_post.html', {'species': WildlifeSpecies.objects.all()})

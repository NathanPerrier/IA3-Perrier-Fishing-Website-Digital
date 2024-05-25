from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Post, PostImages, PostLikes, PostSaved, Comment, CommentLikes
from apps.wildlifeAPI.models import *

def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    fish = Species(species="fish").species_search()
    
    return render(request, 'pages/social/feed.html', {'posts': posts, 'fishes': fish})

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from apps.users.models import Profile

from apps.wildlifeAPI.models import *

def index(request):
    return render(request, "pages/club/index.html")

@login_required
def join(request):
    group = Group.objects.get(name='Member')
    request.user.groups.add(group)
    return redirect('/')
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from apps.users.models import Profile

from apps.users.wrapper import admin_required
from .utils import member_filter
from .forms import MemberAdminForm
from apps.wildlifeAPI.models import *

def index(request):
    return render(request, "pages/club/index.html")

@login_required
def join(request):
    group = Group.objects.get(name='Member')
    request.user.groups.add(group)
    return redirect(request.META.get('HTTP_REFERER'))

@admin_required
def mambers_table(request):

    filters = member_filter(request)
    memebr_group = Group.objects.get(name='Member')
    members_list = memebr_group.user_set.all().filter(**filters)
    form = MemberAdminForm()

    page = request.GET.get('page', 1)
    paginator = Paginator(members_list, 5)
    members = paginator.page(page)

    if request.method == 'POST':
        form = MemberAdminForm(request.POST)
        if form.is_valid():
            return post_request_handling(request, form)

    context = {
        'segment'  : 'members',
        'parent'   : 'apps',
        'form'     : form,
        'members' : members
    }
    
    return render(request, 'apps/members.html', context)



@admin_required
def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_member(request, id):
    member = Group.objects.get(name='Member')
    member.user_set.remove(User.objects.get(id=id))
    return redirect(request.META.get('HTTP_REFERER'))


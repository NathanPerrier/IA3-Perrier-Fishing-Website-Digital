from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from user_visit.models import UserVisit

from apps.tracking.models import *

from .forms import *
from apps.users.wrapper import admin_required
from .utils import *

@admin_required
def routes(request):
    filters = routes_filter(request)
    route_list = Routes.objects.filter(**filters)
    form = RoutesAdminForm()

    page = request.GET.get('page', 1)
    paginator = Paginator(route_list, 5)
    routes = paginator.page(page)

    if request.method == 'POST':
        form = RoutesAdminForm(request.POST)
        if form.is_valid():
            return post_request_handling(request, form)

    context = {
        'routes': routes,
        'segment'  : 'routes',
        'parent'   : 'tracking',
        'form': form,
    }
    return render(request, 'tracking/routes.html', context)

@admin_required
def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_route(request, id):
    route = Routes.objects.get(id=id)
    route.delete()
    return redirect(request.META.get('HTTP_REFERER'))



@admin_required
def login_log(request):
    filters = login_log_filter(request)
    route_list = LoginLog.objects.filter(**filters)
    form = LoginLogAdminForm()

    page = request.GET.get('page', 1)
    paginator = Paginator(route_list, 5)
    logs = paginator.page(page)

    if request.method == 'POST':
        form = LoginLogAdminForm(request.POST)
        if form.is_valid():
            return post_request_handling(request, form)

    context = {
        'logs': logs,
        'segment'  : 'login_log',
        'parent'   : 'tracking',
        'form': form,
    }
    return render(request, 'tracking/login_log.html', context)

@admin_required
def delete_login_log(request, id):
    log = LoginLog.objects.get(id=id)
    log.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@admin_required
def user_visits(request):
    filters = user_visits_filter(request)
    route_list = UserVisit.objects.filter(**filters)
    form = UserVisitAdminForm()

    page = request.GET.get('page', 1)
    paginator = Paginator(route_list, 5)
    visits = paginator.page(page)

    if request.method == 'POST':
        form = UserVisitAdminForm(request.POST)
        if form.is_valid():
            return post_request_handling(request, form)

    context = {
        'visits': visits,
        'segment'  : 'user_visit',
        'parent'   : 'tracking',
        'form': form,
    }
    return render(request, 'tracking/user_visits.html', context)

@admin_required
def delete_user_visit(request, id):
    visit = UserVisit.objects.get(id=id)
    visit.delete()
    return redirect(request.META.get('HTTP_REFERER'))


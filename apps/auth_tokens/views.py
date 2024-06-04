from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.authtoken.models import Token

from .forms import AuthTokenAdminForm
from apps.users.wrapper import admin_required
from .utils import token_filter

@admin_required
def index(request):
    filters = token_filter(request)
    token_list = Token.objects.filter(**filters)
    form = AuthTokenAdminForm()

    page = request.GET.get('page', 1)
    paginator = Paginator(token_list, 5)
    tokens = paginator.page(page)

    if request.method == 'POST':
        form = AuthTokenAdminForm(request.POST)
        if form.is_valid():
            return post_request_handling(request, form)

    context = {
        'tokens': tokens,
        'segment'  : 'tokens',
        'parent'   : 'apps',
        'form': form,
    }
    return render(request, 'apps/tokens.html', context)

@admin_required
def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_token(request, id):
    token = Token.objects.get(id=id)
    token.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@admin_required
def update_token(request, id):
    token = Token.objects.get(id=id)
    if request.method == 'POST':
        token.key = request.POST.get('key')
        token.user = request.POST.get('user')
        token.save()
    return redirect(request.META.get('HTTP_REFERER'))
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *

@login_required(login_url="/users/signin")
def dashboard(request):
  if request.user.is_superuser:
    context = {
      'segment': 'dashboard',
    }
    return render(request, "dashboard/index.html", context)
  return render(request, "pages/errors/404.html")

def index(request):

  context = {}
  return render(request, "pages/index.html", context)

def pricing(request):

  context = {}
  return render(request, "pages/pricing.html", context)

def contact(request):

  context = {}
  return render(request, "pages/contact.html", context)

# ERRORS


def handler404(request, exception):
    return render(request, 'pages/errors/404.html', status=404)

def handler500(request):
    return render(request, 'pages/errors/500.html', status=500)
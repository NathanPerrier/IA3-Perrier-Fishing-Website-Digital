from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *

@login_required
def dashboard(request):

  context = {
    'segment': 'dashboard',
  }
  return render(request, "dashboard/index.html", context)

def index(request):

  context = {}
  return render(request, "pages/index.html", context)

def pricing(request):

  context = {}
  return render(request, "pages/pricing.html", context)



# ERRORS


def handler404(request, exception):
    return render(request, 'pages/errors/404.html', status=404)

def handler500(request):
    return render(request, 'pages/errors/500.html', status=500)
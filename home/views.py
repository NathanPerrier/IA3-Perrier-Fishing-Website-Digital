from django.shortcuts import render


from .models import *

def dashboard(request):

  context = {
    'segment': 'dashboard',
  }
  return render(request, "dashboard/index.html", context)

def index(request):

  context = {}
  return render(request, "pages/index.html", context)
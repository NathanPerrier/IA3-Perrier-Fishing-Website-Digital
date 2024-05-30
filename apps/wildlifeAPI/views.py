from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User

from .models import WildlifeSpecies
from .utils import species_filter
from .wrapper import admin_required
from .forms import SpeciesAdminForm

@admin_required
def datatables(request):
  filters = species_filter(request)
  product_list = WildlifeSpecies.objects.filter(**filters)
  form = SpeciesAdminForm()

  page = request.GET.get('page', 1)
  paginator = Paginator(product_list, 5)
  species = paginator.page(page)

  if request.method == 'POST':
      form = SpeciesAdminForm(request.POST)
      if form.is_valid():
          return specie_request_handling(request, form)

  context = {
    'segment'  : 'species',
    'parent'   : 'apps',
    'form'     : form,
    'species' : species
  }
  
  return render(request, 'apps/species.html', context)



@admin_required
def specie_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_specie(request, id):
    specie = WildlifeSpecies.objects.get(id=id)
    specie.delete()
    return redirect(request.META.get('HTTP_REFERER'))


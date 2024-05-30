from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.datatables, name="species_datatables"),
    path('delete-post/<int:id>/', views.delete_specie, name="delete_specie"),
]
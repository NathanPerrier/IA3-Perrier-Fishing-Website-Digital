from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pricing/", views.pricing, name="pricing"),
    
    path("dashboard/", views.dashboard, name="starter"),
]

# core/urls.py

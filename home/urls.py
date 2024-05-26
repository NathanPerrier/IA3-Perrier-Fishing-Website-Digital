from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pricing/", views.pricing, name="pricing"),
    path("contact/", views.contact, name="contact"),
    path("dashboard/", views.dashboard, name="starter"),
    path("terms-and-conditions/", views.terms_and_conditions, name="terms-and-conditions"),
    path("privacy-policy/", views.privacy_policy, name="privacy-policy"),
]

# core/urls.py

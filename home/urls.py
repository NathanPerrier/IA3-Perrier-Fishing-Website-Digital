from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("dashboard/", views.dashboard, name="starter"),
    path("terms-and-conditions/", views.terms_and_conditions, name="terms-and-conditions"),
    path("privacy-policy/", views.privacy_policy, name="privacy-policy"),
    path("file-upload", views.upload_file, name="file-upload"),
    path("search", views.search, name="search"),
]

# core/urls.py

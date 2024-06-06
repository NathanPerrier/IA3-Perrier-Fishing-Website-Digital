from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('join/', views.join, name='join'),
    path('members/', views.mambers_table, name='members_table'),
    path('delete/<int:id>/', views.delete_member, name='delete_member'),
]
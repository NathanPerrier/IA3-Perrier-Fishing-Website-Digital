from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='auth_tokens'),
    path('<int:pk>/delete/', views.delete_token, name='delete_token'),
    path('<int:pk>/update/', views.update_token, name='update_token'),
]
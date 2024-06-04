from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('routes/', views.routes, name='routes_tracking'),
    path('routes/<int:pk>/delete/', views.delete_route, name='delete_routes_tracking'),

    path('login_log/', views.login_log, name='login_log_tracking'),
    path('login_log/<int:pk>/delete/', views.delete_login_log, name='delete_logs_tracking'),

    path('user_visit/', views.user_visits, name='user_visit_tracking'),
    path('user_visit/<int:pk>/delete/', views.delete_user_visit, name='delete_visits_tracking'),
]
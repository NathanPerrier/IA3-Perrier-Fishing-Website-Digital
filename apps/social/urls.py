from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('feed/', views.feed, name='social_feed'),
    path('post/', views.create_post, name='social_create_post'),
    path('feed/<int:post_id>/comment/', views.create_comment, name='social_create_comment'),
    path('feed/<int:post_id>/comment/<int:comment_id>/comment/', views.create_nested_comment, name='social_create_comment'),
]
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('feed/', views.feed, name='social_feed'),
    path('post/', views.create_post, name='social_create_post'),
    path('feed/<int:post_id>/edit/', views.edit_post, name='social_edit_post'),
    path('feed/<int:post_id>/delete/', views.delete_user_post, name='social_delete_post'),
        
    path('feed/<int:post_id>/comment/', views.create_comment, name='social_create_comment'),
    path('feed/<int:post_id>/comment/<int:comment_id>/comment/', views.create_nested_comment, name='social_create_comment'),
    path('feed/<int:post_id>/like/', views.like_post, name='social_like_post'),
    path('feed/<int:post_id>/comment/<int:comment_id>/like/', views.like_comment, name='social_like_comment'),
    path('feed/<int:post_id>/save/', views.save_post, name='social_save_post'),
    
    path("", views.datatables, name="social_datatables"),
    path('delete-post/<int:id>/', views.delete_post, name="delete_post"),
    path('update-post/<int:id>/', views.update_post, name="update_post"),
]
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.views.generic import CreateView
from apps.social.models import Post
from apps.users.models import Profile, Followers
from apps.users.forms import *
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from apps.users.utils import *
from .wrapper import admin_required





class SignInView(LoginView):
    form_class = SigninForm
    template_name = "authentication/sign-in.html"

class SignUpView(CreateView):
    form_class = SignupForm
    template_name = "authentication/sign-up.html"
    success_url = "/users/signin/"

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'authentication/password-change.html'
    form_class = UserPasswordChangeForm

class UserPasswordResetView(PasswordResetView):
    template_name = 'authentication/forgot-password.html'
    form_class = UserPasswordResetForm

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/reset-password.html'
    form_class = UserSetPasswordForm


def signout_view(request):
    logout(request)
    return redirect(reverse('signin'))


def profile_page(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)

    else:
        if not request.user.is_authenticated: 
            return redirect(reverse('signin'))
        user = request.user 


    profile = get_object_or_404(Profile, user=user)
    
    is_following = False
    
    if request.user.is_authenticated:
        is_following = Followers.objects.filter(follower=request.user.profile, following=profile).exists()

    context = {
        'user': user,
        'profile': profile,
        'profile_posts':  get_profile_posts(request, profile),  
        'saved_posts': get_saved_posts(request, profile),  
        'followers_posts': get_followers_posts(request, profile),
        'following_posts': get_following_posts(request, profile), 
        'suggested_posts': get_suggested_posts(request, profile),
        'suggested_followers': get_suggested_followers(request, profile),
        'followers' : Followers.objects.filter(following=profile).all(),
        'following' : Followers.objects.filter(follower=profile).all(),
        'is_following': is_following,
    }
    return render(request, 'pages/profile.html', context)

@login_required(login_url='/users/signin/')
def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    follower = Followers(follower=request.user.profile, following=profile)
    follower.follow()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/users/signin/')
def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    follower = Followers(follower=request.user.profile, following=profile)
    follower.unfollow()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/users/signin/')
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'segment': 'profile',
    }
    return render(request, 'pages/edit_profile.html', context)



def update_bio(request):
    profile = get_object_or_404(Profile, user=request.user)
    profile.bio = request.POST.get('bio')
    profile.save()
    messages.success(request, 'Bio updated successfully')
    return redirect(request.META.get('HTTP_REFERER'))

def upload_avatar(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        profile.avatar = request.FILES.get('avatar')
        profile.save()
        messages.success(request, 'Avatar uploaded successfully')
    return redirect(request.META.get('HTTP_REFERER'))

def delete_avatar(request):
    profile = get_object_or_404(Profile, user=request.user)
    profile.avatar = None
    profile.save()
    messages.success(request, 'Avatar deleted successfully')
    return redirect(request.META.get('HTTP_REFERER'))

def change_password(request):
    user = request.user
    if request.method == 'POST':
        if check_password(request.POST.get('current_password'), user.password):
            user.set_password(request.POST.get('new_password'))
            user.save()
            messages.success(request, 'Password changed successfully')
        else:
            messages.error(request, "Password doesn't match!")
    return redirect(request.META.get('HTTP_REFERER'))


@admin_required
def user_list(request):
    filters = user_filter(request)
    user_list = User.objects.filter(**filters)
    form = UserForm()

    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 5)
    users = paginator.page(page)

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            return post_request_handling(request, form)

    context = {
        'users': users,
        'form': form,
    }
    return render(request, 'apps/users.html', context)


@admin_required
def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))

@admin_required
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@admin_required
def update_user(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def user_change_password(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.set_password(request.POST.get('password'))
        user.save()
    return redirect(request.META.get('HTTP_REFERER'))


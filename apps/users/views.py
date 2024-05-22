from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.views.generic import CreateView
from apps.common.models import Product #! rm
from apps.social.models import Post
from apps.users.models import Profile, Followers
from apps.users.forms import SigninForm, SignupForm, UserPasswordChangeForm, UserSetPasswordForm, UserPasswordResetForm, ProfileForm
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from apps.users.utils import user_filter


def index(request):

    prodName = ''
    
    if len( Product.objects.all() ):
        prodName = Product.objects.all()[0].name
        
    return HttpResponse("INDEX Users" + ' ' + prodName)



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
    
    context = {
        'user': user,
        'profile': profile,
        'posts':  Post.objects.filter(user_profile=profile),  
        'followers' : Followers.objects.filter(following=profile).all(),
        'following' : Followers.objects.filter(follower=profile).all(),
        'is_following': Followers.objects.filter(follower=request.user.profile, following=profile).exists()
    }
    return render(request, 'pages/profile.html', context)

@login_required(login_url='/users/signin/')
def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    Followers.objects.update_or_create(follower=request.user.profile, following=profile)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/users/signin/')
def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    Followers.objects.filter(follower=request.user.profile, following=profile).delete()
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



def user_list(request):
    filters = user_filter(request)
    user_list = User.objects.filter(**filters)
    form = SignupForm()

    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 5)
    users = paginator.page(page)

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            return post_request_handling(request, form)

    context = {
        'users': users,
        'form': form,
    }
    return render(request, 'apps/users.html', context)


@login_required(login_url='/users/signin/')
def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/users/signin/')
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
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
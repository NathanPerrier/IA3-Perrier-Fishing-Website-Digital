from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from apps.social.models import *

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
    
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'hidden'}), label="Content")
    # images = forms.FileField(label="Image", widget=forms.FileInput(attrs={'multiple': True, 'class': 'hidden'}))
        
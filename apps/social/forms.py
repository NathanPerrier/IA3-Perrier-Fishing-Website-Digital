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
        
        
class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
    

    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            self.fields[field_name].widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'
            self.fields[field_name].widget.attrs['required'] = False
            
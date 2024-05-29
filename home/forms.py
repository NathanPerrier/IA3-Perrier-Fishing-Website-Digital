from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'name@company.com'
    }), label="Email")
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'Let us know how we can help you!'
    }), label="Subject")
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'Leave a comment...'
    }), label="Message")
    
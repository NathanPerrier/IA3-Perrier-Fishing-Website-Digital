from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import ContactForm
from .models import *

@login_required(login_url="/users/signin")
def dashboard(request):
  if request.user.is_superuser:
    context = {
      'segment': 'dashboard',
    }
    return render(request, "dashboard/index-2.html", context)
  return render(request, "pages/errors/404.html")

def index(request):

  context = {}
  return render(request, "pages/index-2.html", context)

def pricing(request):

  context = {}
  return render(request, "pages/pricing.html", context)

def contact(request):
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():  
      try:
        send_mail(
              'Thank Your For Contacting Us!',
              'Thank you for getting in touch with us. We will get back to you as soon as possible. If you have any further questions, please do not hesitate to ask.',
              settings.EMAIL_HOST_USER,
              [form.cleaned_data.get('email')],
              fail_silently=False,
        )
        form=ContactForm()
        messages.success(request, 'Contact Message Sent!')
      except Exception as e: messages.error(request, 'There was an error sending your message. Please try again later.')
    else: messages.error(request, form.errors.as_text()) 
  else: form = ContactForm(initial={'email': request.user.email}) if request.user.is_authenticated else ContactForm()
  return render(request, "pages/contact.html", {'success': False, 'form': form})


def handler404(request, exception):
    return render(request, 'pages/errors/404.html', status=404)

def handler500(request):
    return render(request, 'pages/errors/500.html', status=500)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from .forms import ContactForm
from .models import *
from .utils import *
from apps.users.models import Profile
from user_visit.models import UserVisit
from apps.social.models import *

@login_required(login_url="/users/signin")
def dashboard(request):
  if request.user.is_superuser:
    context = {
      'segment': 'dashboard',
      'posts': Post.objects.all(),
      'profiles': Profile.objects.all(),
      'top_posts': get_top_posts(),
      'top_profiles': get_top_profiles(),
      'posts_by_week': sort_posts_by_week(),
      'user_visits': UserVisit.objects.all()
    }
    return render(request, "dashboard/index.html", context)
  return render(request, "pages/errors/404.html")


def index(request):
  context = {}
  return render(request, "pages/index.html", context)

def search(request):
  filters = profile_filter(request)
  
  try:
    profile = Profile.objects.filter(**filters).first()
  
    return redirect(f'/users/profile/{profile.user.username}')
  
  except:
    return redirect('/users/profiles/')

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

def terms_and_conditions(request):

  context = {}
  return render(request, "pages/policies/terms_and_conditions.html", context)


def privacy_policy(request):
  
    context = {}
    return render(request, "pages/policies/privacy_policy.html", context)

def handler404(request, exception):
    return render(request, 'pages/errors/404.html', status=404)

def handler500(request):
    return render(request, 'pages/errors/500.html', status=500)
  

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        fs = FileSystemStorage()
        
        # Get the existing file_urls from the session, or an empty list if it doesn't exist
        file_urls = request.session.get('file_urls', [])

        for file_name, file in request.FILES.items():
            filename = fs.save(f'posts/images/{clean_name(file.name)}', file)
            file_url = fs.url(filename).replace('media/', '', 1)
            file_urls.append(file_url)
            
        # Save file_urls back to the session
        request.session['file_urls'] = file_urls
        request.session.modified = True
        request.session.save()

        return JsonResponse({'message': 'File uploaded successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)
      
def clean_name(file_name):
    return file_name.replace(' ', '_').replace('(', '').replace('ø', 'o').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace(';', '').replace(':', '').replace('"', '').replace("'", '').replace(',', '').replace('!', '').replace('?', '').replace('#', '').replace('$', '').replace('%', '').replace('^', '').replace('&', '').replace('*', '').replace('-', '_').replace('+', '_').replace('=', '_').replace('/', '_').replace('\\', '_').replace('|', '_').replace('~', '_').replace('`', '_').replace('@', '_').replace('<', '_').replace('>','_')
"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os, random, string
from pathlib        import Path
from dotenv         import load_dotenv
from str2bool       import str2bool
from django.contrib import messages
from datetime       import timedelta

load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))

# Enable/Disable DEBUG Mode
DEBUG = True #str2bool(os.environ.get('DEBUG'))

# Hosts Settings
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://localhost:5085', 'http://127.0.0.1:8000', 'http://127.0.0.1:5085']

# Used by DEBUG-Toolbar 
INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    
    "social_django",
    "user_visit",

    'django_recaptcha',
    'corsheaders',

    "home",
    "apps.users",
    "apps.api", 
    "apps.tasks",
    "apps.wildlifeAPI",
    "apps.social",
    "apps.tracking",
    'apps.microsoft_auth',
    
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',

    "django_celery_results",

    'rest_framework',
    'rest_framework.authtoken', 
    'drf_spectacular',
    'django_api_gen',
    'django_browser_reload',

    "debug_toolbar", # Debug Toolbar
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'apps.microsoft_auth.backends.MicrosoftAuthenticationBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Debug Toolbar
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'user_visit.middleware.UserVisitMiddleware',
    'apps.tracking.routes.main.TrackURLChangeMiddleware',
]

ROOT_URLCONF = "core.urls"

UI_TEMPLATES = os.path.join(BASE_DIR, 'templates') 

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [UI_TEMPLATES],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug", # Debug Toolbar
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'social_django.context_processors.backends', 
                'apps.microsoft_auth.context_processors.microsoft',
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Social Auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET =os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://localhost:8000/social/complete/google-oauth2/' #auth/google/callback'

SOCIAL_AUTH_GITHUB_KEY = os.environ.get('GITHUB_OAUTH2_CLIENT_ID')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('GITHUB_OAUTH2_CLIENT_SECRET')
SOCIAL_AUTH_GITHUB_OAUTH2_REDIRECT_URI = 'http://localhost:8000/social/complete/github/'

MICROSOFT_AUTH_CLIENT_ID = os.environ.get('MICROSOFT_OAUTH2_APP_ID')
MICROSOFT_AUTH_CLIENT_SECRET = os.environ.get('MICROSOFT_OAUTH2_CLIENT_SECRET')
MICROSOFT_AUTH_TENANT_ID = os.environ.get('MICROSOFT_OAUTH2_TENANT_ID')

SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = MICROSOFT_AUTH_CLIENT_SECRET
MICROSOFT_AUTH_AUTO_REPLACE_ACCOUNTS = True
MICROSOFT_AUTH_REDIRECT_URI = 'http://localhost:8000/microsoft/from-auth-redirect/'

# Microsoft authentication
# include Microsoft Accounts, Office 365 Enterpirse and Azure AD accounts
MICROSOFT_AUTH_LOGIN_TYPE = 'ma'

# Xbox Live authentication
# MICROSOFT_AUTH_LOGIN_TYPE = 'xbl'  


#ReCaptcha
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_SITE_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

RECAPTCHA_PROXY = {'http': 'http://127.0.0.1:8000', 'https': 'https://127.0.0.1:8000'}
# RECAPTCHA_DOMAIN = 'www.recaptcha.net'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
DB_USERNAME = os.getenv('DB_USERNAME' , None)
DB_PASS     = os.getenv('DB_PASS'     , None)
DB_HOST     = os.getenv('DB_HOST'     , None)
DB_PORT     = os.getenv('DB_PORT'     , None)
DB_NAME     = os.getenv('DB_NAME'     , None)

if DB_ENGINE and DB_NAME and DB_USERNAME:
    DATABASES = { 
      'default': {
        'ENGINE'  : 'django.db.backends.' + DB_ENGINE, 
        'NAME'    : DB_NAME,
        'USER'    : DB_USERNAME,
        'PASSWORD': DB_PASS,
        'HOST'    : DB_HOST,
        'PORT'    : DB_PORT,
        }, 
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]
CORS_ALLOW_ALL_ORIGINS = True


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

SITE_ID = 1

AUTH_USER_MODEL = 'auth.User'

CUSTOM_GROUPS = ["Admin", "Student", "Teacher", "Parent", "User", "Member", "Staff", "Leader", "Volunteer",
                 "Year 4", "Year 5", "Year 6", "Year 7", "Year 8", "Year 9", "Year 10", "Year 11", "Year 12"]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL  = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ### Async Tasks (Celery) Settings ###

CELERY_SCRIPTS_DIR        = os.path.join(BASE_DIR, "tasks_scripts" )

CELERY_LOGS_URL           = "/tasks_logs/"
CELERY_LOGS_DIR           = os.path.join(BASE_DIR, "tasks_logs"    )

CELERY_BROKER_URL         = os.environ.get("CELERY_BROKER", "redis://localhost:6379")
CELERY_RESULT_BACKEND     = os.environ.get("CELERY_BROKER", "redis://localhost:6379")

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT    = 30 * 60
CELERY_CACHE_BACKEND      = "django-cache"
CELERY_RESULT_BACKEND     = "django-db"
CELERY_RESULT_EXTENDED    = True
CELERY_RESULT_EXPIRES     = 60*60*24*30 # Results expire after 1 month
CELERY_ACCEPT_CONTENT     = ["json"]
CELERY_TASK_SERIALIZER    = 'json'
CELERY_RESULT_SERIALIZER  = 'json'

CELERY_BEAT_SCHEDULE = {
    'clean_data_every_minute': {
        'task': 'apps.wildlifeAPI.celery.clean_data',
        'schedule': timedelta(days=2),  
    },
}
########################################


LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/users/signin/'
#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# ### API-GENERATOR Settings ###
API_GENERATOR = {
    'user'   : "apps.users.models.User",
    'wildlife': "wildlifeAPI.models.*",
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
########################################

# risky
SESSION_COOKIE_HTTPONLY=False

MESSAGE_TAGS = {
    messages.INFO: 'text-blue-800 border border-blue-300 bg-blue-50 dark:text-blue-400 dark:border-blue-800',
    messages.SUCCESS: 'text-green-800 border border-green-300 bg-green-50 dark:text-green-400 dark:border-green-800',
    messages.WARNING: 'text-yellow-800 border border-yellow-300 bg-yellow-50 dark:text-yellow-300 dark:border-yellow-800',
    messages.ERROR: 'text-red-800 border border-red-300 bg-red-50 dark:text-red-400 dark:border-red-800',
}
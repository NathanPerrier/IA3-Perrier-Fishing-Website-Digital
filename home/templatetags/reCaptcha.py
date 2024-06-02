from django.conf import settings
import os
from django import template

register = template.Library()

@register.simple_tag
def get_site_key():
    return settings.RECAPTCHA_PUBLIC_KEY

@register.simple_tag
def get_v3_site_key():
    return os.environ.get('RECAPTCHA_V3_SITE_KEY')

@register.simple_tag
def get_secret_key():
    return settings.RECAPTCHA_PRIVATE_KEY
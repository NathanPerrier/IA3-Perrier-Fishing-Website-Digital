from rest_framework.authtoken.models import Token
from django import template


register = template.Library()

@register.simple_tag
def get_api_token():
    try:
        token = Token.objects.all().first()
        return token.key
    except Token.DoesNotExist:
        return None
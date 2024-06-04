from django import template
from django.conf import settings
import urllib.parse
import os


register = template.Library()

@register.filter
def get_item(list, index):
    try:
        return list[index].common_name if index < len(list) else None
    except KeyError:
        return list[index].common_name if index < len(list) else None
    

@register.filter
def replace_spaces(value):
    return value.replace(' ', '_')


@register.filter
def clean_file(value):
    """
    This function removes the 'C:\\' prefix from the given file path.
    """
    return value.replace('C:\\', '')

@register.filter
def image_exists(value):
    """
    This function checks if the given image exists.
    """
    try:
        return os.path.isfile(os.path.join(f"{settings.MEDIA_ROOT}{(value.replace('/media', '').replace('/', os.sep))}"))

    except (TypeError, OSError) as e:
        print(f"An error occurred: {e}")
        return False
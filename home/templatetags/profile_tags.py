from django import template
from apps.users.models import Profile, Followers

register = template.Library()

@register.filter
def is_following(user, profile):
    return Followers.objects.filter(follower=user, following=profile).exists()
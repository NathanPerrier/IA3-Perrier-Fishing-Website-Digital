from django import template
from apps.users.models import Profile, Followers

register = template.Library()

@register.filter
def is_following(user, profile):
    return Followers.objects.filter(follower=user, following=profile).exists()

@register.filter
def club_authorised(user):
    user_groups = user.groups.values_list('name', flat=True)
    authorized_groups = ['Member', 'Leader', 'Teacher', 'Staff', 'Admin']

    return any(group in user_groups for group in authorized_groups) or user.is_staff or user.is_superuser

@register.filter
def is_club_member(user):
    user_groups = user.groups.values_list('name', flat=True)
    authorized_groups = ['Member', 'Leader', 'Volunteer']

    return any(group in user_groups for group in authorized_groups)

@register.filter
def is_staff(user):
    user_groups = user.groups.values_list('name', flat=True)
    authorized_groups = ['Teacher', 'Staff']
    
    return any(group in user_groups for group in authorized_groups) or user.is_staff

@register.filter
def is_student(user):
    user_groups = user.groups.values_list('name', flat=True)
    authorized_groups = ['Student', "Year 4", "Year 5", "Year 6", "Year 7", "Year 8", "Year 9", "Year 10", "Year 11", "Year 12"]

    return any(group in user_groups for group in authorized_groups)

@register.filter
def is_parent(user):
    user_groups = user.groups.values_list('name', flat=True)
    authorized_groups = ['Parent']

    return any(group in user_groups for group in authorized_groups)

@register.filter
def is_admin(user):
    user_groups = user.groups.values_list('name', flat=True)
    authorized_groups = ['Admin']

    return any(group in user_groups for group in authorized_groups) or user.is_superuser
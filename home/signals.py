from django.contrib.auth.models import User
from apps.users.models import Profile
from django.core.mail import send_mail

from django.db.models.signals import post_save, post_migrate, post_init
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        if instance.is_superuser:
            profile.role = "admin"
            profile.save()
            
        send_mail(
            'Welcome to Ambrose Treacy College!',
            'Thank you for registering with us. We hope you enjoy our services.',
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=True,
        )

@receiver(post_migrate)
def create_custom_groups(sender, **kwargs):
    for group_name in settings.CUSTOM_GROUPS:
        Group.objects.get_or_create(name=group_name)

    print("Custom groups ensured.")
    

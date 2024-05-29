from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from apps.tracking.models import LoginLog

@receiver(user_logged_in)
def log_user_login(sender, user, request, **kwargs):
    LoginLog.objects.create(user=user, ip_address=request.META['REMOTE_ADDR'])
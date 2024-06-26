from django.http import Http404
from django.contrib.auth.decorators import login_required

def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
    return wrapper


def admin_required(view_func):
    """Requires user membership in at least one of the groups passed in."""
    @login_required(login_url='/users/signin/')
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        user_groups = user.groups.values_list('name', flat=True)
        authorized_groups = ['Admin']

        if any(group in user_groups for group in authorized_groups) or user.is_staff or user.is_superuser:
            return view_func(request, *args, **kwargs)

        raise Http404
    return _wrapped_view
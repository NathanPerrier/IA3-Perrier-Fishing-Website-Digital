from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def decorator(view_func):
        @login_required(login_url='/users/signin')
        def _wrapped_view(request, *args, **kwargs):
            if bool(request.user.groups.filter(name__in=group_names)) or request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            raise Http404
        return _wrapped_view
    return decorator
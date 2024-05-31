from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def decorator(view_func):
        @login_required(login_url='/users/signin')
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            user_groups = user.groups.values_list('name', flat=True)
            authorized_groups = ['Member', 'Leader', 'Teacher', 'Staff', 'Admin']

            if any(group in user_groups for group in authorized_groups) or user.is_staff or user.is_superuser:
                return view_func(request, *args, **kwargs)

            raise Http404
        return _wrapped_view
    return decorator

def extended_group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def decorator(view_func):
        @login_required(login_url='/users/signin')
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            user_groups = user.groups.values_list('name', flat=True)
            authorized_groups = ['Student', 'Parent', 'Member', 'Leader', 'Teacher', 'Staff', 'Admin', "Year 4", "Year 5", "Year 6", "Year 7", "Year 8", "Year 9", "Year 10", "Year 11", "Year 12"]

            if any(group in user_groups for group in authorized_groups) or user.is_staff or user.is_superuser:
                return view_func(request, *args, **kwargs)

            raise messages.error(request, 'You do not have permission to comment, please become a club member.')
        return _wrapped_view
    return decorator

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
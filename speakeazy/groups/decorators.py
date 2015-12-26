from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from functools import wraps
from speakeazy.groups.models import Permission


def require_permission(permission):
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            group = self.kwargs['group']
            user = self.request.user

            permissions = Permission.objects.filter(authorization__groupmembership__group__slug=group,
                                                    authorization__groupmembership__user=user).values_list('name',
                                                                                                           flat=True)

            if not permissions:
                raise Http404('Group not found')

            if permission not in permissions:
                raise PermissionDenied()

            return fn(self, *args, **kwargs)

        return wrapper

    return decorator

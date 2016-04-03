from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from speakeazy.groups.models import Group


class GroupPermissiondMixin(object):
    """
    View mixin which verifies that the user is authenticated.

    NOTE: This should be the left-most mixin of a view after the LoginRequiredMixin.
    """

    group_permission = None
    group = None
    permissions = None

    # cache these
    def dispatch(self, request, *args, **kwargs):
        self.group = get_object_or_404(Group, slug=kwargs['group'])
        user = request.user

        self.permissions = set(user.groupmembership_set.filter(group=self.group) \
                               .values_list('authorizations__permissions__name', flat=True))

        if self.group_permission:
            if not self.permissions:
                raise Http404('Group not found')

            if self.group_permission not in self.permissions:
                raise PermissionDenied()

        return super(GroupPermissiondMixin, self).dispatch(request, *args, **kwargs)

from django.shortcuts import get_object_or_404
from speakeazy.groups.models import Group


class GroupPermissiondMixin(object):
    """
    View mixin which verifies that the user is authenticated.

    NOTE:
        This should be the left-most mixin of a view after the LoginRequiredMixin.
    """

    group_permission = None
    group = None

    # cache these
    def dispatch(self, request, *args, **kwargs):
        self.group = get_object_or_404(Group, slug=kwargs['group'])
        user = request.user

        # permissions = user.groupmembership_set.filter(group=self.group).values_list(
        #     'authorizations__permissions__name', flat=True)
        #
        # if not permissions:
        #     raise Http404('Group not found')
        #
        # if self.group_permission not in permissions:
        #     raise PermissionDenied()

        return super(GroupPermissiondMixin, self).dispatch(request, *args, **kwargs)


LIST_AUDIENCE = 'list_audience'
VIEW_AUDIENCE = 'view_audience'
ADD_AUDIENCE = 'add_audience'
UPDATE_AUDIENCE = 'update_audience'
DELETE_AUDIENCE = 'delete_audience'

LIST_USER = 'list_user'
VIEW_USER = 'view_user'
UPDATE_USER = 'update_user'
DELETE_USER = 'delete_user'

LIST_INVITE = 'list_invite'
VIEW_INVITE = 'view_invite'
ADD_INVITE = 'add_invite'
UPDATE_INVITE = 'update_invite'
DELETE_INVITE = 'delete_invite'

LIST_SUBMISSION = 'list_submission'
VIEW_SUBMISSION = 'view_submission'
ADD_SUBMISSION = 'add_submission'
UPDATE_SUBMISSION = 'update_submission'
DELETE_SUBMISSION = 'delete_submission'

# LIST_ = 'list_'
# VIEW_ = 'view_'
# ADD_ = 'add_'
# UPDATE_ = 'update_'
# DELETE_ = 'delete_'

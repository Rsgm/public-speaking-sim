from speakeazy.groups.models import GroupMembership

from braces.views import LoginRequiredMixin
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from vanilla.model_views import DetailView, ListView, DeleteView, UpdateView


class ListUsers(LoginRequiredMixin, ListView):
    template_name = 'speakeazy/groups/user/list.html'

    def get_queryset(self):
        group = self.kwargs['group']
        authorize(group, 'list_users', self.request.session)
        return GroupMembership.objects.filter(group=group)


class AddUser(LoginRequiredMixin, DetailView):
    model = GroupMembership
    template_name = 'speakeazy/groups/user/view.html'

    def get_object(self):
        group = self.kwargs['group']
        user = self.kwargs['user']

        authorize(group, 'view_user', self.request.session)

        return get_object_or_404(GroupMembership, group=group, user=user)

class ViewUser(LoginRequiredMixin, DetailView):
    model = GroupMembership
    template_name = 'speakeazy/groups/user/view.html'

    def get_object(self):
        group = self.kwargs['group']
        user = self.kwargs['user']

        authorize(group, 'view_user', self.request.session)

        return get_object_or_404(GroupMembership, group=group, user=user)


class UpdateUser(LoginRequiredMixin, UpdateView):
    model = GroupMembership
    template_name = 'speakeazy/groups/user/update.html'

    fields = ['authorization']

    def get_object(self):
        group = self.kwargs['group']
        user = self.kwargs['user']

        authorize(group, 'update_user', self.request.session)

        return get_object_or_404(GroupMembership, group=group, user=user)


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = GroupMembership
    template_name = 'speakeazy/groups/user/delete.html'

    def get_object(self):
        group = self.kwargs['group']
        user = self.kwargs['user']

        authorize(group, 'delete_user', self.request.session)

        return get_object_or_404(GroupMembership, group=group, user=user)


# move to inheritable class
def authorize(group, permission, session):
    if group not in session:
        raise Http404("Group does not exist.")

    if permission not in session[group].permissions:
        raise Http404("Unauthorized")

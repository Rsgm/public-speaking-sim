from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from speakeazy.groups.decorators import require_permission
from speakeazy.groups.models import GroupMembership
from vanilla.model_views import DetailView, ListView, DeleteView, UpdateView


class ListUsers(LoginRequiredMixin, ListView):
    template_name = 'speakeazy/groups/user/list.html'

    @require_permission('list_users')
    def get_queryset(self):
        group = self.kwargs['group']
        return GroupMembership.objects.filter(group=group)


# class AddUser(LoginRequiredMixin, DetailView):
#     model = GroupMembership
#     template_name = 'speakeazy/groups/user/view.html'
#
#     @require_permission('add_users')
#     def get_object(self):
#         group = self.kwargs['group']
#         user = self.kwargs['user']
#         return get_object_or_404(GroupMembership, group=group, user=user)
#

class ViewUser(LoginRequiredMixin, DetailView):
    model = GroupMembership
    template_name = 'speakeazy/groups/user/view.html'

    @require_permission('view_users')
    def get_object(self):
        group = self.kwargs['group']
        user = self.kwargs['user']
        return get_object_or_404(GroupMembership, group=group, user=user)


class UpdateUser(LoginRequiredMixin, UpdateView):
    model = GroupMembership
    template_name = 'speakeazy/groups/user/update.html'

    fields = ['authorization']

    @require_permission('update_users')
    def get_object(self):
        group = self.kwargs['group']
        user = self.kwargs['user']
        return get_object_or_404(GroupMembership, group=group, user=user)


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = GroupMembership
    template_name = 'speakeazy/groups/user/delete.html'

    @require_permission('delete_users')
    def get_object(self):
        group = self.kwargs['group']
        user = self.kwargs['user']
        return get_object_or_404(GroupMembership, group=group, user=user)

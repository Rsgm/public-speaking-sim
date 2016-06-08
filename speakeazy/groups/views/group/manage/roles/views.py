from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from vanilla.model_views import DetailView, ListView, DeleteView, UpdateView

from speakeazy.groups.mixins import GroupMixin
from speakeazy.groups.models import GroupMembership
from speakeazy.groups.permissions import LIST_USER, VIEW_USER, UPDATE_USER, DELETE_USER
from speakeazy.groups.views.group.manage.user import UpdateForm


class List(LoginRequiredMixin, GroupMixin, ListView):
    model = GroupMembership
    context_object_name = 'membership_list'
    template_name = 'groups/group/user/list.html'

    group_permission = LIST_USER

    def get_queryset(self):
        group = self.kwargs['group']
        return GroupMembership.objects.filter(group__slug=group)


class Manage(LoginRequiredMixin, GroupMixin, ListView):
    model = GroupMembership
    context_object_name = 'membership_list'
    template_name = 'groups/group/user/list.html'

    group_permission = LIST_USER

    def get_queryset(self):
        group = self.kwargs['group']
        return GroupMembership.objects.filter(group__slug=group)


class View(LoginRequiredMixin, GroupMixin, DetailView):
    model = GroupMembership
    context_object_name = 'membership'
    template_name = 'groups/group/user/view.html'

    group_permission = VIEW_USER

    def get_object(self):
        group = self.kwargs['group']
        user = self.kwargs['user']
        return get_object_or_404(GroupMembership, group__slug=group, user=user)


class Update(LoginRequiredMixin, GroupMixin, UpdateView):
    model = GroupMembership
    context_object_name = 'membership'
    form_class = UpdateForm
    template_name = 'groups/group/user/update.html'

    fields = ['roles']

    group_permission = UPDATE_USER

    def get_object(self):
        group = self.kwargs['group']
        user = self.kwargs['user']
        return get_object_or_404(GroupMembership, group__slug=group, user=user)


class Delete(LoginRequiredMixin, GroupMixin, DeleteView):
    model = GroupMembership
    context_object_name = 'membership'
    template_name = 'groups/group/user/delete.html'

    group_permission = DELETE_USER

    def get_object(self):
        group = self.kwargs['group']
        user = self.kwargs['user']
        return get_object_or_404(GroupMembership, group__slug=group, user=user)

    def get_success_url(self):
        return reverse_lazy('groups:group:user:list', kwargs={'group': self.group.slug})

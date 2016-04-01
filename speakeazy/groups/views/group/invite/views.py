from string import ascii_lowercase

from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from random import choice
from speakeazy.groups.mixins import GroupPermissiondMixin
from speakeazy.groups.permissions import LIST_INVITE, VIEW_INVITE, ADD_INVITE, UPDATE_INVITE, DELETE_INVITE
from speakeazy.groups.models import GroupInvite
from speakeazy.groups.views.group.invite.forms import UpdateForm, AddForm
from vanilla.model_views import DetailView, ListView, DeleteView, UpdateView, CreateView


class List(LoginRequiredMixin, GroupPermissiondMixin, ListView):
    model = GroupInvite
    context_object_name = 'invite_list'
    template_name = 'groups/group/invite/list.html'

    group_permission = LIST_INVITE

    def get_queryset(self):
        group = self.kwargs['group']
        return GroupInvite.objects.filter(group__slug=group)


class View(LoginRequiredMixin, GroupPermissiondMixin, DetailView):
    model = GroupInvite
    context_object_name = 'invite'
    template_name = 'groups/group/invite/view.html'

    group_permission = VIEW_INVITE

    def get_object(self):
        group = self.kwargs['group']
        invite = self.kwargs['invite']
        return get_object_or_404(GroupInvite, group__slug=group, slug=invite)


class Add(LoginRequiredMixin, GroupPermissiondMixin, CreateView):
    model = GroupInvite
    form_class = AddForm
    template_name = 'groups/group/invite/add.html'

    group_permission = ADD_INVITE

    def get_form(self, data=None, files=None, **kwargs):
        return AddForm(self.group, data=data, files=files, **kwargs)

    def form_valid(self, form):
        form.instance.token = self.random_token(self.group.pk)

        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def random_token(self, group):
        """
        Generates a unique token for a group.
        Note: This will keep generating tokens until a unique one is found.
        :param group: the group to
        :return: a token of length TOKEN_LENGTH
        """
        token_length = 6
        string = ''

        for n in range(token_length):
            string += choice(ascii_lowercase)

        if GroupInvite.objects.filter(group=group, token=string).count() > 0:
            return self.random_token(group)

        return string


class Update(LoginRequiredMixin, GroupPermissiondMixin, UpdateView):
    model = GroupInvite
    # context_object_name = 'invite'
    form_class = UpdateForm
    template_name = 'actions/update.html'

    group_permission = UPDATE_INVITE

    def get_object(self):
        group = self.kwargs['group']
        invite = self.kwargs['invite']
        object = get_object_or_404(GroupInvite, group__slug=group, slug=invite)
        return object


class Delete(LoginRequiredMixin, GroupPermissiondMixin, DeleteView):
    model = GroupInvite
    context_object_name = 'invite'
    template_name = 'groups/group/invite/delete.html'

    group_permission = DELETE_INVITE

    def get_object(self):
        group = self.kwargs['group']
        invite = self.kwargs['invite']
        return get_object_or_404(GroupInvite, group__slug=group, slug=invite)

    def get_success_url(self):
        return reverse_lazy('groups:group:invite:list', kwargs={'group': self.group.slug})

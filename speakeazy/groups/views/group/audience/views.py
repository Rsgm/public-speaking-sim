from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from speakeazy.groups.mixins import GroupPermissiondMixin
from speakeazy.groups.permissions import LIST_AUDIENCE, VIEW_AUDIENCE, ADD_AUDIENCE, UPDATE_AUDIENCE, DELETE_AUDIENCE
from speakeazy.groups.models import Audience
from speakeazy.groups.views.group.audience.forms import UpdateForm, AddForm
from vanilla.model_views import DetailView, ListView, DeleteView, UpdateView, CreateView


class List(LoginRequiredMixin, GroupPermissiondMixin, ListView):
    model = Audience
    context_object_name = 'audience_list'
    template_name = 'groups/group/audience/list.html'

    group_permission = LIST_AUDIENCE

    def get_queryset(self):
        group = self.kwargs['group']
        return Audience.objects.filter(group__slug=group)


class View(LoginRequiredMixin, GroupPermissiondMixin, DetailView):
    model = Audience
    context_object_name = 'audience'
    template_name = 'groups/group/audience/view.html'

    group_permission = VIEW_AUDIENCE

    def get_object(self):
        group = self.kwargs['group']
        audience = self.kwargs['audience']
        return get_object_or_404(Audience, group__slug=group, slug=audience)


class Add(LoginRequiredMixin, GroupPermissiondMixin, CreateView):
    model = Audience
    form_class = AddForm
    template_name = 'groups/group/audience/add.html'

    group_permission = ADD_AUDIENCE

    # add group to form
    # convert video, upload to storage


class Update(LoginRequiredMixin, GroupPermissiondMixin, UpdateView):
    model = Audience
    context_object_name = 'audience'
    form_class = UpdateForm
    template_name = 'groups/group/audience/update.html'

    group_permission = UPDATE_AUDIENCE

    def get_object(self):
        group = self.kwargs['group']
        audience = self.kwargs['audience']
        return get_object_or_404(Audience, group__slug=group, slug=audience)


class Delete(LoginRequiredMixin, GroupPermissiondMixin, DeleteView):
    model = Audience
    context_object_name = 'audience'
    template_name = 'groups/group/audience/delete.html'

    group_permission = DELETE_AUDIENCE

    def get_object(self):
        group = self.kwargs['group']
        audience = self.kwargs['audience']
        return get_object_or_404(Audience, group__slug=group, slug=audience)

    def get_success_url(self):
        return reverse_lazy('groups:group:audience:list', kwargs={'group': self.group.slug})

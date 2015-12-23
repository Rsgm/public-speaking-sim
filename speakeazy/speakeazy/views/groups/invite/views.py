from braces.views import LoginRequiredMixin
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from speakeazy.speakeazy.models import GroupMembership, GroupInvite
from vanilla.model_views import DetailView, ListView, CreateView, DeleteView, UpdateView


class ListInvite(LoginRequiredMixin, ListView):
    template_name = 'speakeazy/groups/invite/list.html'

    def get_queryset(self):
        group = self.kwargs['group']
        authorize(group, 'list_invite', self.request.session)
        return GroupInvite.objects.filter(group=group)


class ViewInvite(LoginRequiredMixin, DetailView):
    model = GroupInvite
    template_name = 'speakeazy/groups/invite/view.html'

    def get_object(self):
        group = self.kwargs['group']
        slug = self.kwargs['slug']

        authorize(group, 'view_invite', self.request.session)

        return get_object_or_404(GroupInvite, group=group, slug=slug)


def authorize(group, permission, session):
    if group not in session:
        raise Http404("Group does not exist.")

    if permission not in session[group].permissions:
        raise Http404("Unauthorized")

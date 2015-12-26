from speakeazy.groups.models import GroupInvite

from braces.views import LoginRequiredMixin
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from vanilla.model_views import DetailView, ListView


class ListInvites(LoginRequiredMixin, ListView):
    template_name = 'groups/group/invite/list.html'

    def get_queryset(self):
        group = self.kwargs['group']

        return GroupInvite.objects.filter(group=group)


class ViewInvite(LoginRequiredMixin, DetailView):
    model = GroupInvite
    template_name = 'groups/group/invite/view.html'

    def get_object(self):
        group = self.kwargs['group']
        slug = self.kwargs['slug']

        return get_object_or_404(GroupInvite, group=group, slug=slug)

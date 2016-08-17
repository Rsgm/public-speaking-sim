from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from speakeazy.groups.mixins import GroupMixin
from speakeazy.groups.models import Submission
from speakeazy.groups.permissions import VIEW_SUBMISSION, LIST_SUBMISSION, UPDATE_SUBMISSION, DELETE_SUBMISSION
from vanilla.model_views import DetailView, ListView, UpdateView, DeleteView


class List(LoginRequiredMixin, GroupMixin, ListView):
    template_name = 'groups/group/submission/list.html'
    model = Submission

    group_permission = LIST_SUBMISSION

    def get_queryset(self):
        group = self.kwargs['group']
        return Submission.objects.filter(group__slug=group).select_related('recording__project__user') \
            .order_by('created_time')


class View(LoginRequiredMixin, GroupMixin, DetailView):
    template_name = 'groups/group/submission/view.html'
    model = Submission

    group_permission = VIEW_SUBMISSION


class Update(LoginRequiredMixin, GroupMixin, UpdateView):
    template_name = 'groups/group/submission/update.html'
    model = Submission
    fields = ['group', 'recording', 'grader', 'finished']

    group_permission = UPDATE_SUBMISSION


class Delete(LoginRequiredMixin, GroupMixin, DeleteView):
    template_name = 'groups/group/submission/delete.html'
    model = Submission

    group_permission = DELETE_SUBMISSION

    def get_success_url(self):
        return reverse_lazy('groups:group:submission:list', kwargs={'group': self.group.slug})

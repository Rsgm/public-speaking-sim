from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from speakeazy.groups.mixins import GroupPermissiondMixin
from speakeazy.groups.permissions import VIEW_SUBMISSION, DELETE_SUBMISSION, \
    EVALUATE_SUBMISSION, LIST_SUBMISSION
from speakeazy.groups.models import Submission
from speakeazy.recordings.models import EvaluationType, Evaluation
from vanilla.model_views import DetailView, ListView, DeleteView
from vanilla.views import TemplateView


class List(LoginRequiredMixin, GroupPermissiondMixin, ListView):
    template_name = 'groups/group/submission/list.html'
    model = Submission

    group_permission = LIST_SUBMISSION

    def get_queryset(self):
        group = self.kwargs['group']
        return Submission.objects.filter(group__slug=group)


class View(LoginRequiredMixin, GroupPermissiondMixin, DetailView):
    template_name = 'groups/group/submission/view.html'
    model = Submission

    group_permission = VIEW_SUBMISSION


# class Add(LoginRequiredMixin, GroupPermissiondMixin, CreateView):
#     template_name = 'groups/group/submission/add.html'
#     model = Submission
#     form_class = AddForm
#
#     group_permission = ADD_SUBMISSION
#
#     def get_form(self, data=None, files=None, **kwargs):
#         return AddForm(self.group, data=data, files=files, **kwargs)
#
#     def form_valid(self, form):
#         group = form.instance['token']
#         form.instance['token'] = self.random_token(group.pk)
#
#         self.object = form.save()
#         return HttpResponseRedirect(self.get_success_url())
#
#     def random_token(self, group):
#         """
#         Generates a unique token for a group.
#         Note: This will keep generating tokens until a unique one is found.
#         :param group:
#         :return: a token of length TOKEN_LENGTH
#         """
#         TOKEN_LENGTH = 6
#         string = ''
#
#         for n in range(TOKEN_LENGTH):
#             string += choice(ascii_lowercase)
#
#         if Submission.objects.filter(group=group, token=string).count() > 0:
#             return self.random_token(group)
#
#         return string


# class Update(LoginRequiredMixin, GroupPermissiondMixin, UpdateView):
#     template_name = 'actions/update.html'
#     model = Submission
#     form_class = UpdateForm
#
#     group_permission = UPDATE_SUBMISSION


class Delete(LoginRequiredMixin, GroupPermissiondMixin, DeleteView):
    template_name = 'groups/group/submission/delete.html'
    model = Submission

    group_permission = DELETE_SUBMISSION

    def get_success_url(self):
        return reverse_lazy('groups:group:submission:list', kwargs={'group': self.group.slug})


class GraderRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('recordings:recording:view', kwargs={'type': 'grader', 'key': kwargs['key']})


class Evaluate(LoginRequiredMixin, GroupPermissiondMixin, TemplateView):
    template_name = 'groups/group/evaluation/evaluate_view.html'
    group_permission = EVALUATE_SUBMISSION

    def get_context_data(self, **kwargs):
        submission = self.kwargs['pk']

        kwargs['view'] = self
        kwargs['group'] = self.group

        # todo: allow viewing submissions that are not started xor started by the current user
        kwargs['submission'] = get_object_or_404(Submission, group=self.group, pk=submission)
        kwargs['evaluation_type_list'] = EvaluationType.objects.all()

        return kwargs

    def post(self, request, *args, **kwargs):
        submission = kwargs['pk']

        post = request.POST
        text = post['text']
        eval_type = post['type']
        seconds = int(post['seconds'])

        submission = get_object_or_404(Submission, group=self.group, pk=submission, for_evaluation=True)

        recording = submission.recording

        evaluation_type = get_object_or_404(EvaluationType, name=eval_type)

        evaluation = Evaluation(evaluator=request.user,
                                recording=recording,
                                type=evaluation_type,
                                text=text,
                                seconds=seconds)
        evaluation.save()

        return HttpResponse()

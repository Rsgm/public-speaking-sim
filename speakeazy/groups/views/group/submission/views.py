from string import ascii_lowercase

from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from random import choice
from speakeazy.groups.mixins import GroupPermissiondMixin, LIST_INVITE, VIEW_INVITE, ADD_INVITE, UPDATE_INVITE, \
    DELETE_INVITE, EVALUATE_SUBMISSION
from speakeazy.groups.models import Submission, SUBMISSION_READY
from speakeazy.groups.views.group.invite.forms import UpdateForm, AddForm
from speakeazy.recordings.models import EvaluationType, Evaluation
from vanilla.model_views import DetailView, ListView, DeleteView, UpdateView, CreateView
from vanilla.views import TemplateView


class List(LoginRequiredMixin, GroupPermissiondMixin, ListView):
    template_name = 'groups/group/invite/list.html'
    model = Submission

    group_permission = LIST_INVITE

    def get_queryset(self):
        group = self.kwargs['group']
        return Submission.objects.filter(group__slug=group)


class View(LoginRequiredMixin, GroupPermissiondMixin, DetailView):
    template_name = 'groups/group/invite/view.html'
    model = Submission

    group_permission = VIEW_INVITE


class Add(LoginRequiredMixin, GroupPermissiondMixin, CreateView):
    template_name = 'groups/group/invite/add.html'
    model = Submission
    form_class = AddForm

    group_permission = ADD_INVITE

    def get_form(self, data=None, files=None, **kwargs):
        return AddForm(self.group, data=data, files=files, **kwargs)

    def form_valid(self, form):
        group = form.instance['token']
        form.instance['token'] = self.random_token(group.pk)

        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def random_token(self, group):
        """
        Generates a unique token for a group.
        Note: This will keep generating tokens until a unique one is found.
        :param group:
        :return: a token of length TOKEN_LENGTH
        """
        TOKEN_LENGTH = 6
        string = ''

        for n in range(TOKEN_LENGTH):
            string += choice(ascii_lowercase)

        if Submission.objects.filter(group=group, token=string).count() > 0:
            return self.random_token(group)

        return string


class Update(LoginRequiredMixin, GroupPermissiondMixin, UpdateView):
    template_name = 'actions/update.html'
    model = Submission
    form_class = UpdateForm

    group_permission = UPDATE_INVITE


class Delete(LoginRequiredMixin, GroupPermissiondMixin, DeleteView):
    template_name = 'groups/group/invite/delete.html'
    model = Submission

    group_permission = DELETE_INVITE

    def get_success_url(self):
        return reverse('groups:group:invite:list', kwargs={'group': self.group.slug})


class Evaluate(LoginRequiredMixin, GroupPermissiondMixin, TemplateView):
    template_name = 'groups/group/evaluation/evaluate_view.html'
    group_permission = EVALUATE_SUBMISSION

    def get_context_data(self, **kwargs):
        submission = self.kwargs['pk']

        kwargs['view'] = self
        kwargs['group'] = self.group

        # todo: allow viewing submissions that are not started xor started by the current user
        kwargs['submission'] = get_object_or_404(Submission,
                                                 group=self.group,
                                                 pk=submission,
                                                 for_evaluation=True,
                                                 state=SUBMISSION_READY)
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

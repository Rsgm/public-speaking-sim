# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from speakeazy.groups.mixins import ADD_SUBMISSION
from speakeazy.groups.models import Group, GroupMembership, Submission

from speakeazy.projects.models import Recording

from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from speakeazy.recordings.models import EvaluationType, Evaluation
from vanilla.views import TemplateView

EVALUATION = 'eval'
EVALUATION_REQUEST = 'request'


class RecordingView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/project/recording_view.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        kwargs['recording'] = get_object_or_404(
            Recording.objects.filter(project__user=self.request.user,
                                     project__slug=self.kwargs['project'],
                                     slug=self.kwargs['recording']))

        kwargs['evaluation_type_list'] = EvaluationType.objects.all()
        kwargs['evaluation_list'] = Evaluation.objects.filter(recording=kwargs['recording'])
        kwargs['group_list'] = Group.objects.filter(groupmembership__user=self.request.user,
                                                    groupmembership__authorizations__permissions__name=ADD_SUBMISSION)

        return kwargs

    def post(self, request, *args, **kwargs):
        recording = get_object_or_404(Recording,
                                      project__user=request.user,
                                      project__slug=kwargs['project'],
                                      slug=kwargs['recording'])

        if request.POST['action'] == EVALUATION:
            return self.evaluate(request, recording)

        elif request.POST['action'] == EVALUATION_REQUEST:
            return self.request_evaluation(request, recording)

    def evaluate(self, request, recording):

        post = request.POST
        evaluation_type = get_object_or_404(EvaluationType, name=post['type'])

        evaluation = Evaluation(evaluator=request.user,
                                recording=recording,
                                type=evaluation_type,
                                text=post['text'],
                                seconds=int(post['seconds']))
        evaluation.save()

        return HttpResponse()

    def request_evaluation(self, request, recording):
        post = request.POST

        membership = GroupMembership.objects.filter(group__pk=post['group'],
                                                    user=request.user,
                                                    authorizations__permissions__name=ADD_SUBMISSION) \
            .select_related('group')

        if not membership:
            raise Http404('No group found.')

        group = membership.get().group

        submission = Submission()
        submission.group = group
        submission.recording = recording
        submission.for_evaluation = True
        submission.save()

        return HttpResponse()

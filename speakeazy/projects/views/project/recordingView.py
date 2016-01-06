# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from speakeazy.groups.mixins import ADD_SUBMISSION
from speakeazy.groups.models import Group

from speakeazy.projects.models import Recording

from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from speakeazy.recordings.models import EvaluationType, Evaluation
from vanilla.views import TemplateView


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

        post = request.POST
        evaluation_type = get_object_or_404(EvaluationType, name=post['type'])

        evaluation = Evaluation(evaluator=request.user,
                                recording=recording,
                                type=evaluation_type,
                                text=post['text'],
                                seconds=int(post['seconds']))
        evaluation.save()

        return HttpResponse()

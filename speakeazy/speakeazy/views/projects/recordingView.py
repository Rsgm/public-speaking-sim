# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from speakeazy.speakeazy.models import Project, Recording, Evaluation, EvaluationType
from vanilla.model_views import DetailView
from vanilla.views import TemplateView


class RecordingView(LoginRequiredMixin, TemplateView):
    template_name = 'speakeazy/projects/recording_view.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        kwargs['recording'] = get_object_or_404(
            Recording.objects.filter(project__user=self.request.user, project__slug=self.kwargs['project'],
                                     slug=self.kwargs['recording']))
        kwargs['evaluation_type_list'] = EvaluationType.objects.all()

        return kwargs


@login_required
def create_evaluation(request, *args, **kwargs):
    recording = get_object_or_404(Recording, project__user=request.user, project__slug=kwargs['project'],
                                  slug=kwargs['recording'])

    post = request.POST
    evaluation_type = get_object_or_404(EvaluationType, name=post['type'])
    evaluation = Evaluation(evaluator=request.user, recording=recording, type=evaluation_type, text=post['text'],
                            seconds=int(post['seconds']))
    evaluation.save()

    return HttpResponse()

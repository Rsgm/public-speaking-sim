# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from speakeazy.recordings.models import EvaluationType, Evaluation, Recording
from speakeazy.util.views import PostView


class Create(LoginRequiredMixin, PostView):
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

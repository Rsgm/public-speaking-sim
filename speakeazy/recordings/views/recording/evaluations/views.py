# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from speakeazy.recordings.mixins import RecordingAuthorizationMixin
from speakeazy.recordings.models import EvaluationType, Evaluation
from speakeazy.util.views import PostView


class Create(RecordingAuthorizationMixin, PostView):
    def post(self, request, *args, **kwargs):
        post = request.POST
        evaluation_type = get_object_or_404(EvaluationType, name=post['type'])

        evaluation = Evaluation(evaluator=request.user,
                                recording=self.recording,
                                type=evaluation_type,
                                text=post['text'],
                                seconds=int(post['seconds']))
        evaluation.save()

        return HttpResponse()

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from speakeazy.recordings.mixins import RecordingMixin
from speakeazy.recordings.models import EvaluationType, Evaluation
from speakeazy.util.email import send_feedback_email
from speakeazy.util.views import PostView


class Create(RecordingMixin, PostView):
    def post(self, request, *args, **kwargs):
        post = request.POST
        evaluation_type = get_object_or_404(EvaluationType, name=post['type'])

        evaluation = Evaluation(evaluator=request.user,
                                recording=self.recording,
                                type=evaluation_type,
                                text=post['text'],
                                seconds=int(post['seconds']))
        evaluation.save()

        if self.submission:
            send_feedback_email(self.submission, request.user)

        return HttpResponse()

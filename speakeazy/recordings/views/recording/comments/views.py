# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.http.response import HttpResponse

from speakeazy.recordings.mixins import RecordingMixin
from speakeazy.recordings.models import Comment
from speakeazy.util.email import send_feedback_email
from speakeazy.util.views import PostView


class Create(RecordingMixin, PostView):
    def post(self, request, *args, **kwargs):
        comment = Comment(user=request.user, recording=self.recording, text=request.POST['text'])
        comment.save()

        send_feedback_email(self.submission, request.user)

        return HttpResponse()


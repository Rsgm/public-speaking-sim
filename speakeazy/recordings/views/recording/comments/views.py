# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from speakeazy.recordings.models import Recording, Comment
from speakeazy.util.views import PostView


class Create(LoginRequiredMixin, PostView):
    def post(self, request, *args, **kwargs):
        recording = get_object_or_404(Recording,
                                      project__user=request.user,
                                      project__slug=kwargs['project'],
                                      slug=kwargs['recording'])

        comment = Comment(user=request.user, recording=recording, text=request.POST['text'])
        comment.save()

        return HttpResponse()

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import jwt
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from vanilla.views import TemplateView

from speakeazy.projects.models import UserProject
from speakeazy.recordings import models
from speakeazy.recordings.models import Recording, UploadPiece
from speakeazy.recordings.tasks import convert_media, concatenate_media

START = 'start'
UPLOAD = 'upload'
FINISH = 'finish'

PRIVATE_KEY = open(settings.JWT_KEYFILE_PATH, 'r').read()


class Record(LoginRequiredMixin, TemplateView):
    template_name = 'recordings/record.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self
        kwargs['project'] = get_object_or_404(UserProject, user=self.request.user, slug=self.kwargs['project'])
        return kwargs

    @method_decorator(sensitive_post_parameters('a', 'v'))
    def post(self, request, *args, **kwargs):
        project_slug = kwargs['project']

        if request.POST['request'] == START:
            return self.start(project_slug, request)

        elif request.POST['request'] == UPLOAD:
            recording_pk = request.POST['recording']
            return self.upload(project_slug, recording_pk, request)

        elif request.POST['request'] == FINISH:
            recording_pk = request.POST['recording']
            return self.finish(project_slug, recording_pk, request)

        else:
            raise Http404()

    def start(self, project_slug, request):
        project = get_object_or_404(UserProject, user=request.user, slug=project_slug)
        # create recording
        recording = Recording(project=project)
        recording.save()

        data = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60),
            'aud': 'speakeazy:recording',
            'id': recording.pk,
        }

        token = jwt.encode(data, PRIVATE_KEY, algorithm='ES512')
        return HttpResponse(token)

    # @ratelimit(key='user', rate='2/4s', block=True)
    def upload(self, project_slug, recording_pk, request):
        # todo: test for bad requests, is it even needed?
        # find recording
        recording = get_object_or_404(Recording,
                                      project__user=request.user,
                                      project__slug=project_slug,
                                      pk=recording_pk,
                                      state=models.RECORDING_UPLOADING)

        # create object to keep the id
        piece = UploadPiece(recording=recording)
        piece.save()

        # write video data
        if 'v' in request.POST:
            video = open('%s/%s.b64' % (settings.RECORDING_PATHS['VIDEO_PIECES'], piece.id), 'w')
            video.write(request.POST['v'])
            video.close()

        # write video data
        if 'a' in request.POST:
            audio = open('%s/%s.b64' % (settings.RECORDING_PATHS['AUDIO_PIECES'], piece.id), 'w')
            audio.write(request.POST['a'])
            audio.close()

        # start converting the piece
        convert_media.delay(piece.id)
        return HttpResponse()

    def finish(self, project_slug, recording_pk, request):
        recording = get_object_or_404(Recording,
                                      project__user=request.user,
                                      project__slug=project_slug,
                                      pk=recording_pk,
                                      state=models.RECORDING_UPLOADING)
        # get piece list
        piece_list = UploadPiece.objects.filter(recording=recording).values_list('pk', flat=True)

        # run concat task
        concatenate_media.delay(recording.pk, piece_list)

        messages.info(request, _('Your recording is processing, check back in a few seconds.'), fail_silently=True)
        return HttpResponse(recording.project.get_absolute_url())

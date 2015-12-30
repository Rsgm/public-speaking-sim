# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from speakeazy.projects.models import Project
from speakeazy.recordings import models
from speakeazy.recordings.models import Recording, UploadPiece
from speakeazy.recordings.tasks import convert_media, concatenate_media
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from ratelimit.decorators import ratelimit
from vanilla.views import TemplateView


class Record(LoginRequiredMixin, TemplateView):
    template_name = 'recordings/record.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self
        kwargs['project'] = get_object_or_404(Project, user=self.request.user, slug=self.kwargs['project'])
        return kwargs


@login_required
def start(request, *args, **kwargs):
    project = get_object_or_404(Project, user=request.user, slug=kwargs['project'])

    # create recording
    slug = 1 + Recording.objects.filter(project=project).count()
    recording = Recording(project=project, slug=slug)
    recording.save()

    return JsonResponse({'id': recording.slug})


@login_required
@ratelimit(key='ip', rate='2/s', block=True)
def upload(request, *args, **kwargs):
    # todo: test for bad requests, is it even needed?

    # find recording
    recording = get_object_or_404(Recording, project__user=request.user, project__slug=kwargs['project'],
                                  slug=kwargs['recording'], state=models.UPLOADING)

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


@login_required
def finish(request, *args, **kwargs):
    recording = get_object_or_404(Recording, project__user=request.user, project__slug=kwargs['project'],
                                  slug=kwargs['recording'], state=models.UPLOADING)

    # get piece list
    piece_list = UploadPiece.objects.filter(recording=recording).values_list('pk', flat=True)

    # run concat task
    concatenate_media.delay(recording.id, piece_list)

    return HttpResponse()

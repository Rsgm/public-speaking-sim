# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from pathlib import Path

import shutil
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from speakeazy.projects.models import UserProject
from speakeazy.recordings import models
from speakeazy.recordings.models import Recording, UploadPiece
from speakeazy.recordings.tasks import convert_media, concatenate_media
from speakeazy.util.views import PostView
from vanilla.views import TemplateView

START = 'start'
UPLOAD = 'upload'
FINISH = 'finish'


class Record(LoginRequiredMixin, TemplateView):
    template_name = 'recordings/record.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self
        kwargs['project'] = get_object_or_404(UserProject, user=self.request.user, slug=self.kwargs['project'])
        return kwargs

    def post(self, request, *args, **kwargs):
        project_slug = kwargs['project']

        project = get_object_or_404(UserProject, user=request.user, slug=project_slug)
        # create recording
        recording = Recording(project=project)
        recording.save()

        return JsonResponse({'id': recording.pk})

    def put(self, request, *args, **kwargs):
        project_slug = kwargs['project']
        recording_pk = request.POST['recording']
        queryset = Recording.objects.all().filter(project__user=request.user,
                                                  project__slug=project_slug,
                                                  pk=recording_pk,
                                                  state=models.RECORDING_UPLOADING).select_related('recording_set')
        recording = get_object_or_404(queryset)
        # get piece list
        piece_list = queryset.recording_set

        # get server ip for ftp
        ip = None

        # run concat task
        concatenate_media.delay(recording.pk, piece_list, ip)

        messages.info(request, _('Your recording is processing, check back in a few seconds.'))
        return HttpResponse(recording.project.get_absolute_url())

    def delete(self, request, *args, **kwargs):
        project_slug = kwargs['project']
        recording_pk = request.POST['recording']

        Recording.objects.filter(project__user=request.user,
                                 project__slug=project_slug,
                                 pk=recording_pk,
                                 state=models.RECORDING_UPLOADING).delete()
        return HttpResponse()


def write_file(file, path):
    """
    Write uploaded files. This will move the file if possible, otherwise write it from memory.
    Files should not be written to memory if at all possible.

    :param file:
    :param path: pathlib path object pointing to where the file should be written
    """

    if file is TemporaryUploadedFile:
        shutil.move(file.temporary_file_path(), path.absolute())  # todo: does this break django?
    else:  # fallback if not using
        with path.open(mode='wb') as output_file:
            for line in file:
                output_file.write(line)


class PieceUpload(LoginRequiredMixin, PostView):
    # @ratelimit(key='user', rate='2/4s', block=True)
    @method_decorator(sensitive_post_parameters('a', 'v'))
    def post(self, request, *args, **kwargs):
        project_slug = kwargs['project']
        recording_pk = kwargs['recording']

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
        if 'video' in request.FILES:
            path = Path('%s/%s.webm' % (settings.RECORDING_PATHS['VIDEO_PIECES'], piece.pk))
            write_file(request.FILES['video'], path)

        # write audio data
        if 'audio' in request.FILES:
            path = Path('%s/%s.wav' % (settings.RECORDING_PATHS['AUDIO_PIECES'], piece.pk))
            write_file(request.FILES['audio'], path)

        return HttpResponse()

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery.canvas import group
from speakeazy.projects.models import UserProject
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

START = 'start'
UPLOAD = 'upload'
FINISH = 'finish'


# @ratelimit(key='ip', rate='120/m', block=True)
class Record(LoginRequiredMixin, TemplateView):
    template_name = 'recordings/record.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self
        kwargs['project'] = get_object_or_404(UserProject, user=self.request.user, slug=self.kwargs['project'])
        return kwargs

    def post(self, request, *args, **kwargs):
        project_slug = kwargs['project']

        if request.POST['request'] == START:
            return self.start(project_slug, request)

        elif request.POST['request'] == UPLOAD:
            recording_slug = request.POST['recording']
            return self.upload(project_slug, recording_slug, request)

        elif request.POST['request'] == FINISH:
            recording_slug = request.POST['recording']
            return self.finish(project_slug, recording_slug, request)

    def start(self, project_slug, request):
        project = get_object_or_404(UserProject, user=request.user, slug=project_slug)
        # create recording
        slug = 1 + Recording.objects.filter(project=project).count()
        recording = Recording(project=project, slug=slug)
        recording.save()

        return JsonResponse({'id': recording.slug})

    def upload(self, project_slug, recording_slug, request):
        # todo: test for bad requests, is it even needed?
        # find recording
        recording = get_object_or_404(Recording,
                                      project__user=request.user,
                                      project__slug=project_slug,
                                      slug=recording_slug,
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

    def finish(self, project_slug, recording_slug, request):
        recording = get_object_or_404(Recording,
                                      project__user=request.user,
                                      project__slug=project_slug,
                                      slug=recording_slug,
                                      state=models.RECORDING_UPLOADING)
        # get piece list
        piece_list = UploadPiece.objects.filter(recording=recording).values_list('pk', flat=True)

        # run concat task
        concatenate_media.delay(recording.id, piece_list)
        return HttpResponse(recording.project.get_absolute_url())

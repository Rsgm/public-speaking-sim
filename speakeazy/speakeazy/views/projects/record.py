# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from datetime import datetime
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from ratelimit.decorators import ratelimit
from speakeazy.speakeazy import models
from speakeazy.speakeazy.models import Recording, Project, UploadPiece
from speakeazy.speakeazy.tasks import convert_media, concatenate_media
from vanilla.views import TemplateView


class Record(LoginRequiredMixin, TemplateView):
    template_name = 'speakeazy/projects/record.html'


@login_required
def start(request, *args, **kwargs):
    allowed = auth(request, kwargs['project'])
    if not allowed[0]:
        return allowed[1]

    project = allowed[1]

    # create recording
    recording = Recording(project=project)
    recording.save()

    return JsonResponse({'id': recording.slug})


@csrf_exempt
@login_required
@ratelimit(key='ip', rate='1/s', block=True)
def upload(request, *args, **kwargs):  # this may haunt me later on, use rtp, how to auth?
    # maybe use a custom upload handler that limits filesize
    request.upload_handlers = [TemporaryFileUploadHandler()]
    return _upload(request, *args, **kwargs)


@csrf_protect
def _upload(request, *args, **kwargs):
    allowed = auth(request, kwargs['project'])
    if not allowed[0]:
        return allowed[1]

    # todo: test for bad requests

    # find project and recording
    project = allowed[1]
    recording = Recording.objects.filter(project=project, slug=kwargs['recording']).get()

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
    allowed = auth(request, kwargs['project'])
    if not allowed[0]:
        return allowed[1]

    # find project and recording
    project = allowed[1]
    recording = Recording.objects.filter(project=project, slug=kwargs['recording']).get()

    # get piece list
    piece_list = UploadPiece.objects.filter(recording=recording).values_list('pk', flat=True)

    # run concat task
    concatenate_media.delay(recording.id, piece_list)

    # update recording
    recording.finish_time = datetime.now()
    recording.state = models.FINISHED
    recording.save()

    return HttpResponse()


# Authenticate a user
def auth(request, project_slug):
    # find project
    project = Project.objects.filter(user=request.user, slug=project_slug).get()

    # if no project exists, return a redirect
    if not project:
        return False, redirect(reverse('speakeazy:projects:projectList'))

    # return the project
    return True, project

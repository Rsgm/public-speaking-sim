# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from speakeazy.speakeazy.models import Recording, Project, UploadPiece
from speakeazy.speakeazy.tasks import convert_media
from vanilla.views import TemplateView


class Record(LoginRequiredMixin, TemplateView):
    model = Recording
    template_name = 'speakeazy/projects/recording.html'

    # These next two lines tell the view to index lookups by project
    slug_field = "project"
    slug_url_kwarg = "project"


def start(request, project):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    project_name = project
    project = Project.objects.filter(slug=project_name)

    if request.user.id != project.user.id:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # recording.
    # recording = Recording(name=)

    return HttpResponse()


@csrf_exempt
def upload(request, *args, **kwargs):  # this may haunt me later on, use rtp
    # maybe use a custom upload handler that limits filesize
    request.upload_handlers = [TemporaryFileUploadHandler()]
    return _upload(request, *args, **kwargs)


@csrf_protect
def _upload(request, *args, **kwargs):
    # rate limit
    # test for bad requests

    # create object to keep the id
    piece = UploadPiece()
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


def finish(request):
    return HttpResponse()

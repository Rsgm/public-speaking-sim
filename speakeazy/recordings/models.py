# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.base import Model
from speakeazy.users.models import User

UPLOADING = 'u'
PROCESSING = 'p'  # may not be needed
FINISHED = 'r'
STATE_CHOICES = [
    (UPLOADING, 'uploading'),
    (PROCESSING, 'processing'),
    (FINISHED, 'finished')
]


class Recording(Model):
    project = models.ForeignKey('projects.Project', editable=False)  # not sure why this needs to be a string

    state = models.CharField(max_length=1, choices=STATE_CHOICES, default=UPLOADING)
    finish_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)

    duration = models.IntegerField(null=True, blank=True)

    video = models.FileField(upload_to='recordings', null=True, blank=True)
    thumbnail_image = models.FileField(upload_to='thumbnails', null=True, blank=True)
    thumbnail_video = models.FileField(upload_to='thumbnails', null=True, blank=True)

    slug = models.IntegerField()

    def __str__(self):
        return '%s - %s' % (self.project, self.slug)

    def get_absolute_url(self):
        return reverse('speakeazy:projects:recordingView', kwargs={'recording': self.slug})


class UploadPiece(Model):
    recording = models.ForeignKey('Recording')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

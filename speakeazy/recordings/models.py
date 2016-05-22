# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
from django.db.models.base import Model
from django.utils.translation import ugettext_lazy as _

RECORDING_UPLOADING = 'u'
RECORDING_PROCESSING = 'p'  # may not be needed
RECORDING_FINISHED = 'f'
RECORDING_STATE_CHOICES = [
    (RECORDING_UPLOADING, 'uploading'),
    (RECORDING_PROCESSING, 'processing'),
    (RECORDING_FINISHED, 'finished')
]


class Recording(Model):
    project = models.ForeignKey('projects.UserProject', editable=False)

    state = models.CharField(max_length=1, choices=RECORDING_STATE_CHOICES, default=RECORDING_UPLOADING)
    finish_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)

    duration = models.IntegerField(null=True, blank=True)

    video = models.FileField(upload_to='recordings', null=True, blank=True)
    thumbnail_image = models.FileField(upload_to='thumbnails', null=True, blank=True)
    thumbnail_video = models.FileField(upload_to='thumbnails', null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.project, self.pk)

    def get_absolute_url(self):
        '''
        Don't use for shared videos
        '''
        return reverse_lazy ('recordings:recording:view', kwargs={'type': 'owner', 'key': self.pk})


class UploadPiece(Model):
    recording = models.ForeignKey('Recording')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class EvaluationType(Model):
    name = models.CharField(unique=True, max_length=30)
    # description = models.CharField(unique=True, max_length=120)
    # color = models.CharField(unique=True, max_length=6)
    icon_class = models.CharField(unique=True, max_length=40)

    def __str__(self):
        return self.name


class Evaluation(Model):
    evaluator = models.ForeignKey('users.User', null=True, blank=True)
    recording = models.ForeignKey(Recording)

    type = models.ForeignKey('EvaluationType', null=True, blank=True)
    text = models.TextField()
    seconds = models.IntegerField(null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)

    submission = models.ForeignKey('groups.Submission', null=True, blank=True)

    def __str__(self):
        return '%s - %s - %s' % (self.recording, self.seconds, self.type)


class Comment(Model):
    user = models.ForeignKey('users.User')
    recording = models.ForeignKey(Recording)

    text = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.recording, self.user)


# user authorization may be a better name
class SharedUser(Model):
    recording = models.ForeignKey('Recording')
    user = models.ForeignKey('users.User')

    comments = models.BooleanField(_('Users may comment'))
    evaluations = models.BooleanField(_('Users may evaluate'))

    def __str__(self):
        return '%s - %s' % (self.recording, self.user)


# link authorization may be a better name
class SharedLink(Model):
    recording = models.ForeignKey('Recording')
    uuid = models.UUIDField(unique=True)

    comments = models.BooleanField(_('Users may comment'))
    evaluations = models.BooleanField(_('Users may evaluate'))

    login_required = models.BooleanField(_('Users must be logged in'))
    uses = models.IntegerField(_('Amount of times this link can be used'), null=True, blank=True)
    expires = models.DateTimeField(_('The date this link expires'), null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.recording, self.user)

# todo: SharedGroup

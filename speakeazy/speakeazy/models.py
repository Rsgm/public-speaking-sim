# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from autoslug.fields import AutoSlugField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.base import Model
from django.utils.translation import ugettext_lazy as _
from speakeazy.users.models import User

ADMIN = 'a'
GRADER = 'g'
USER = 'u'
ROLES = [
    (ADMIN, 'admin'),
    (GRADER, 'grader'),
    (USER, 'speakeazy'),
]

UPLOADING = 'u'
PROCESSING = 'p'
FINISHED = 'r'
STATE_CHOICES = [
    (UPLOADING, 'uploading'),
    (PROCESSING, 'processing'),
    (FINISHED, 'finished')
]


class Project(Model):
    user = models.ForeignKey(User, editable=False)
    name = models.CharField(_("Name of project"), max_length=30)
    description = models.CharField(_("Description of project"), blank=True, max_length=255)
    audience = models.ForeignKey('Audience', editable=False)

    created_time = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    slug = AutoSlugField(populate_from='name', unique_with='user')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('speakeazy:projects:projectDetail', kwargs={'project': self.slug})


class Recording(Model):
    project = models.ForeignKey('Project', editable=False)

    state = models.CharField(max_length=1, choices=STATE_CHOICES, default=UPLOADING)
    finish_time = models.DateTimeField()
    start_time = models.DateTimeField(auto_now_add=True)

    slug = AutoSlugField(unique_with='project')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('speakeazy:projects:recordingDetail', kwargs={'recording': self.slug})


class Audience(Model):
    name = models.CharField(_("Name of audience"), max_length=60)
    description = models.CharField(_("Description of project"), blank=True, max_length=255)

    user_created = models.BooleanField()
    group = models.ForeignKey('Group')

    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name


class UploadPiece(Model):
    recording = models.ForeignKey('Recording')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class Group(Model):
    name = models.CharField(_("Name of group"), max_length=30)
    description = models.CharField(_("Description of group"), blank=True, max_length=255)

    parent_group = models.ForeignKey('Group', blank=True, null=True)

    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('speakeazy:groups:groupDetail', kwargs={'group': self.slug})


class GroupRole(Model):
    group = models.ForeignKey('Group')
    role = models.CharField(max_length=1, choices=ROLES, default=USER)
    user = models.ForeignKey(User)

    def __str__(self):
        return '%s - %s - %s' % (self.group, self.role, self.user)


class Submission(Model):
    recording = models.ForeignKey('Recording')
    group = models.ForeignKey('Group')

    for_evaluation = models.BooleanField()
    role_visibility = models.CharField(max_length=1, choices=ROLES)

    slug = AutoSlugField(populate_from='recording.project.name', unique_with='group')

    def __str__(self):
        return '%s - %s' % (self.recording.project.user, self.recording.project.name)

    def get_absolute_url(self):
        return reverse('speakeazy:groups:submissionDetail', kwargs={'submission': self.slug})

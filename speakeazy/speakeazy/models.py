# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from autoslug.fields import AutoSlugField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.base import Model
from django.utils.translation import ugettext_lazy as _
from docutils.parsers.rst.directives import choice
from speakeazy.users.models import User

UPLOADING = 'u'
PROCESSING = 'p'  # may not be needed
FINISHED = 'r'
STATE_CHOICES = [
    (UPLOADING, 'uploading'),
    (PROCESSING, 'processing'),
    (FINISHED, 'finished')
]


class Project(Model):
    user = models.ForeignKey(User, editable=False)
    name = models.CharField(_("Name of project"), max_length=30)
    description = models.TextField(_("Description of project"), null=True, blank=True)
    audience = models.ForeignKey('Audience', editable=False)

    created_time = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    slug = AutoSlugField(populate_from='name', unique_with='user')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('speakeazy:projects:projectView', kwargs={'project': self.slug})


class Recording(Model):
    project = models.ForeignKey('Project', editable=False)

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


class Audience(Model):
    name = models.CharField(_("Name of audience"), max_length=60)
    description = models.TextField(_("Description of project"), null=True, blank=True)

    file = models.FileField(upload_to='audience')  # ensure file name uniqueness
    group = models.ForeignKey('Group')

    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name


class UploadPiece(Model):
    recording = models.ForeignKey('Recording')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Group(Model):
    name = models.CharField(_("Name of group"), max_length=30)
    description = models.TextField(_("Description of group"), null=True, blank=True)
    users = models.ManyToManyField(User, through='GroupMembership')

    parent_user_group = models.ForeignKey('self', blank=True, null=True)

    slug = AutoSlugField(populate_from='name', unique=True)

    password = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('speakeazy:groups:groupDetail', kwargs={'group': self.slug})


class GroupMembership(Model):
    group = models.ForeignKey('Group')
    user = models.ForeignKey(User)

    authorization = models.ManyToManyField('Authorization')

    def __str__(self):
        return '%s - %s' % (self.group.name, self.user)


class Authorization(Model):
    name = models.CharField(_("Name of authorization"), max_length=30, unique=True)

    group = models.ForeignKey('Group')
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.name


class Permission(Model):
    name = models.CharField(_("Name of permission"), max_length=30, unique=True)

    def __str__(self):
        return self.name


class Submission(Model):
    recording = models.ForeignKey('Recording')
    group = models.ForeignKey('Group')

    for_evaluation = models.BooleanField()
    group_visibility = models.ForeignKey('Authorization')

    slug = AutoSlugField(populate_from='recording.project.name', unique_with='group')

    def __str__(self):
        return '%s - %s' % (self.recording.project.user, self.recording.project.name)

    def get_absolute_url(self):
        return reverse('speakeazy:groups:submissionDetail', kwargs={'submission': self.slug})


class DefaultAuthorization(Model):
    name = models.CharField(_("Name of authorization"), max_length=30, unique=True)
    description = models.TextField(_("Description of authorization"), null=True, blank=True)
    permissions = models.ManyToManyField('Permission', related_name='+')

    def __str__(self):
        return self.name


class DefaultGroupStructure(Model):
    name = models.CharField(_("Name of group structure"), max_length=30, unique=True)
    description = models.TextField(_("Description of group structure"), null=True, blank=True)
    default_authorization_types = models.ManyToManyField('DefaultAuthorization')

    def __str__(self):
        return self.name


class GroupInvite(Model):
    group = models.ForeignKey('Group')
    token = models.CharField(unique=True, max_length=20)

    uses = models.IntegerField()
    expires = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.group, self.token)


class EvaluationType(Model):
    name = models.CharField(unique=True, max_length=30)
    color = models.CharField(unique=True, max_length=6)
    fa_class = models.CharField(unique=True, max_length=30)

    def __str__(self):
        return self.name


class Evaluation(Model):
    evaluator = models.ForeignKey(User, null=True, blank=True)
    recording = models.ForeignKey('Recording')

    type = models.ForeignKey('EvaluationType')
    text = models.TextField()
    seconds = models.IntegerField()

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s- %s' % (self.recording, self.seconds, self.type)

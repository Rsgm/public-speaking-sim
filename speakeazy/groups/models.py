# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from autoslug.fields import AutoSlugField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.base import Model
from django.utils.translation import ugettext_lazy as _
from speakeazy.recordings.models import Recording
from speakeazy.users.models import User


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
    recording = models.ForeignKey(Recording)
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

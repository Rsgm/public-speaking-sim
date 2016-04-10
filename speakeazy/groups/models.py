# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from autoslug.fields import AutoSlugField
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.db.models.base import Model
from django.utils.translation import ugettext_lazy as _
from speakeazy.groups.permissions import PERMISSIONS
from speakeazy.users.models import User


# SUBMISSION_READY = 'r'
# SUBMISSION_IN_PROGRESS = 'i'
# SUBMISSION_FINISHED = 'f'
# SUBMISSION_STATE_CHOICES = [
#     (SUBMISSION_READY, 'ready'),
#     (SUBMISSION_IN_PROGRESS, 'in progress'),
#     (SUBMISSION_FINISHED, 'finished')
# ]


class Group(Model):
    name = models.CharField(_("Name of group"), max_length=30)
    description = models.TextField(_("Description of group"), null=True, blank=True)
    users = models.ManyToManyField(User, through='GroupMembership')

    parent_user_group = models.ForeignKey('self', blank=True, null=True)
    logo = models.FileField(upload_to='group-logos', null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('groups:group:groupView', kwargs={'group': self.slug})


class GroupMembership(Model):
    group = models.ForeignKey('Group')
    user = models.ForeignKey(User)

    authorizations = models.ManyToManyField('Authorization', blank=True)

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.group.name, self.user)

    def get_absolute_url(self):
        return reverse_lazy('groups:group:user:view', kwargs={'group': self.group.slug, 'user': self.user_id})


class Authorization(Model):
    name = models.CharField(_("Name of authorization"), max_length=30)

    group = models.ForeignKey('Group')
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return '%s - %s' % (self.group, self.name)


class Permission(Model):
    name = models.CharField(_("Name of permission"), max_length=30, unique=True, choices=PERMISSIONS)

    def __str__(self):
        return self.name


class Audience(Model):
    name = models.CharField(_("Name of audience"), max_length=60)
    description = models.TextField(_("Description of audience"), null=True, blank=True)

    file_webm = models.FileField(upload_to='audience', null=True, blank=True)  # ensure file name uniqueness
    file_mp4 = models.FileField(upload_to='audience', null=True, blank=True)  # ensure file name uniqueness
    group = models.ForeignKey('Group')

    slug = AutoSlugField(populate_from='name', unique_with='group', unique=True)

    def __str__(self):
        return self.name


class Submission(Model):
    group = models.ForeignKey('Group')
    recording = models.ForeignKey('recordings.Recording')
    grader = models.ForeignKey('users.User', null=True, blank=True)

    finished = models.BooleanField(default=False)

    # group_visibility = models.ForeignKey('Authorization', null=True, blank=True)  # does nothing currently

    # does nothing currently
    # state = models.CharField(max_length=1, choices=SUBMISSION_STATE_CHOICES, default=SUBMISSION_READY)

    created_time = models.DateTimeField(auto_now_add=True)
    # slug = AutoSlugField(populate_from='recording__project__name', unique_with='group')

    # def __str__(self):
    #     return '%s - %s' % (self.recording.project, self.recording.project.name)

    def get_absolute_url(self):
        return reverse_lazy('groups:group:submission:view', kwargs={'group': Group.slug, 'submission': self.slug})


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

    name = models.CharField(_("Name of invite"), max_length=30)
    description = models.TextField(_("Description of invite"), null=True, blank=True)

    token = models.CharField(max_length=16)
    authorizations = models.ManyToManyField('Authorization', related_name='+', blank=True)

    uses = models.IntegerField(null=True, blank=True)
    expires = models.DateTimeField(null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='name', unique_with='group')

    def get_absolute_url(self):
        return reverse_lazy('groups:group:invite:view', kwargs={'group': self.group.slug, 'invite': self.slug})

    def __str__(self):
        return '%s - %s' % (self.group, self.token)


class SignupMembership(Model):
    group = models.OneToOneField('Group')  # not needed since the group is in authorizations
    authorizations = models.ManyToManyField('Authorization', related_name='+', blank=True)

    def __str__(self):
        return '%s' % self.group.name

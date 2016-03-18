# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from autoslug.fields import AutoSlugField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.base import Model
from django.utils.translation import ugettext_lazy as _
from speakeazy.recordings.models import Recording
from speakeazy.users.models import User


class Project(Model):
    name = models.CharField(_("Name of project"), max_length=30)
    description = models.TextField(_("Description of project"), null=True, blank=True)
    audience = models.ForeignKey('groups.Audience')

    created_time = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    slug = AutoSlugField(populate_from='name', unique_with='user')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class UserProject(Project):
    user = models.ForeignKey(User)

    def get_absolute_url(self):
        return reverse('projects:project:projectView', kwargs={'project': self.slug})


class Settings(Model):
    project = models.OneToOneField('UserProject')
    audience = models.ForeignKey('groups.Audience')

    last_updated = models.DateTimeField(auto_now=True)
    due_date = models.DateField()

    slug = AutoSlugField(populate_from='name', unique_with='user')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:project:projectView', kwargs={'project': self.slug})

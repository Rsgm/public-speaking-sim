# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from autoslug.fields import AutoSlugField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.base import Model
from django.utils.translation import ugettext_lazy as _
from speakeazy.groups.models import Group, Audience
from speakeazy.recordings.models import Recording
from speakeazy.users.models import User


class Project(Model):
    user = models.ForeignKey(User)
    name = models.CharField(_("Name of project"), max_length=30)
    description = models.TextField(_("Description of project"), null=True, blank=True)
    audience = models.ForeignKey(Audience)

    created_time = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    slug = AutoSlugField(populate_from='name', unique_with='user')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:project:projectView', kwargs={'project': self.slug})


class EvaluationType(Model):
    name = models.CharField(unique=True, max_length=30)
    descritpion = models.CharField(unique=True, max_length=120)
    color = models.CharField(unique=True, max_length=6)
    icon_class = models.CharField(unique=True, max_length=40)

    def __str__(self):
        return self.name


class Evaluation(Model):
    evaluator = models.ForeignKey(User, null=True, blank=True)
    recording = models.ForeignKey(Recording)

    type = models.ForeignKey('EvaluationType')
    text = models.TextField()
    seconds = models.IntegerField()

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s- %s' % (self.recording, self.seconds, self.type)

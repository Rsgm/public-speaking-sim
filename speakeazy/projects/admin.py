# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from speakeazy.projects.models import Project, Audience, EvaluationType, Evaluation

admin.site.register(Project)
admin.site.register(Audience)
admin.site.register(EvaluationType)
admin.site.register(Evaluation)

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from speakeazy.projects.models import Project, Settings

admin.site.register(Project)
admin.site.register(Settings)

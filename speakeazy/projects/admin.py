# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from speakeazy.projects.models import Settings, UserProject

admin.site.register(UserProject)
admin.site.register(Settings)

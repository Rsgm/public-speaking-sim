# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from speakeazy.projects.models import Settings, UserProject, PracticeProject, PracticeSpeech

admin.site.register(UserProject)
admin.site.register(PracticeProject)
admin.site.register(PracticeSpeech)
admin.site.register(Settings)

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from speakeazy.recordings.models import Recording, UploadPiece

admin.site.register(Recording)
admin.site.register(UploadPiece)

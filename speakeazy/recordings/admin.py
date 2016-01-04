# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from speakeazy.recordings.models import Recording, UploadPiece, EvaluationType, Evaluation

admin.site.register(Recording)
admin.site.register(UploadPiece)
admin.site.register(EvaluationType)
admin.site.register(Evaluation)

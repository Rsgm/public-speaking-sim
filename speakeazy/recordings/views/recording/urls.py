# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from speakeazy.recordings.views.record import Record
from speakeazy.recordings.views.recording.views import View

urlpatterns = [
    url(
        regex=r'^view/$',
        view=View.as_view(),
        name='view'
    ),

    url(r'^comments/', include("speakeazy.recordings.views.recording.comments.urls", namespace="comments")),
    url(r'^comments/', include("speakeazy.recordings.views.recording.evaluations.urls", namespace="evaluations")),
]

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from speakeazy.recordings.views.record import Record

urlpatterns = [
    url(
        regex=r'^record/(?P<project>[\w-]+)/$',
        view=Record.as_view(),
        name='record'
    ),

    url(r'^r/(?P<project>[\w-]+)/(?P<recording>\d+)/',
        include("speakeazy.recordings.views.recording.urls", namespace="recording")),
]

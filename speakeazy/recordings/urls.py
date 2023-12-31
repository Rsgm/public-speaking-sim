# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from speakeazy.recordings.views.record import Record, PieceUpload

urlpatterns = [
    url(
        regex=r'^record/(?P<project>[\w-]+)/$',
        view=Record.as_view(),
        name='record'
    ),

    url(
        regex=r'^record/(?P<project>[\w-]+)/(?P<recording>[\d]+)/piece/$',
        view=PieceUpload.as_view(),
        name='piece_upload'
    ),

    url(r'^view/(?P<type>[\w]+)/(?P<key>\d+)/',
        include("speakeazy.recordings.views.recording.urls", namespace="recording")),

    url(r'^settings/(?P<pk>\d+)/',
        include("speakeazy.recordings.views.settings.urls", namespace="settings")),
]

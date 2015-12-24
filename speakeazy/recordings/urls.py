# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.recordings.views import Record, start, upload, finish

urlpatterns = [
    url(
        regex=r'^record/$',
        view=Record.as_view(),
        name='record'
    ),

    url(
        regex=r'^/record/start/$',
        view=start,
        name='recordStart'
    ),

    url(
        regex=r'^record/(?P<recording>[\w-]+)/upload/$',
        view=upload,
        name='recordUpload'
    ),

    url(
        regex=r'^record/(?P<recording>[\w-]+)/finish/$',
        view=finish,
        name='recordFinish'
    ),
]

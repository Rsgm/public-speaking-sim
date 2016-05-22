# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from speakeazy.recordings.views.record import Record
from speakeazy.recordings.views.recording.comments.views import Create

urlpatterns = [
    url(
        regex=r'^create/$',
        view=Create.as_view(),
        name='create'
    ),
]

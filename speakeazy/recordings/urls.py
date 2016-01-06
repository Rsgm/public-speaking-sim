# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.recordings.view import Record

urlpatterns = [
    url(
        regex=r'^$',
        view=Record.as_view(),
        name='record'
    ),
]

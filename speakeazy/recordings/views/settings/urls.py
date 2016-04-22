# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.recordings.views.settings.views import Delete, CreateGroupSubmission

urlpatterns = [
    url(
        regex=r'^delete/$',
        view=Delete.as_view(),
        name='delete'
    ),

    url(
        regex=r'^submission/$',
        view=CreateGroupSubmission.as_view(),
        name='submission'
    ),
]

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.projects.views.project.projectView import ProjectView
from speakeazy.projects.views.project.recordingView import RecordingView

urlpatterns = [
    url(
        regex=r'^$',
        view=ProjectView.as_view(),
        name='projectView'
    ),

    url(
        regex=r'^(?P<recording>\d+)/$',
        view=RecordingView.as_view(),
        name='recordingView'
    ),  # since recording slugs are always numbers, it will not collide with /record or others
]

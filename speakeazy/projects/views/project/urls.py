# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.generic.base import RedirectView
from speakeazy.projects.views.project.projectView import ProjectView
from speakeazy.recordings.views.recording.views import View

urlpatterns = [
    url(
        regex=r'^$',
        view=ProjectView.as_view(),
        name='projectView'
    ),

    url(
        regex=r'^(?P<recording>\d+)/$',
        view=RedirectView.as_view(pattern_name='recordings:recording:view', permanent=True),
        name='recordingView'
    ),
]

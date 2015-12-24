# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.projects.views.projects.projectView import ProjectView
from speakeazy.projects.views.projects.recordingView import RecordingView, create_evaluation

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

    url(
        regex=r'^(?P<recording>\d+)/evaluate/$',
        view=create_evaluation,
        name='recordingEvaluation'
    ),

    # url(
    #     regex=r'^view/(?P<email>\S+)/$',
    #     view=,
    #     name=''
    # ),
]

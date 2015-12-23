# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.speakeazy.views.projects.projectView import ProjectView
from speakeazy.speakeazy.views.projects.record import Record, start, upload, finish
from speakeazy.speakeazy.views.projects.recordingView import RecordingView, create_evaluation

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

    # url(
    #     regex=r'^view/(?P<email>\S+)/$',
    #     view=,
    #     name=''
    # ),
]

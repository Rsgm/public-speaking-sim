# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from speakeazy.speakeazy.views.projects.projectDetail import ProjectDetail
from speakeazy.speakeazy.views.projects.projectList import ProjectList
from speakeazy.speakeazy.views.projects.record import Record, start, upload, finish

urlpatterns = [
    url(
        regex=r'^$',
        view=ProjectList.as_view(),
        name='projectList'
    ),

    url(
        regex=r'^(?P<project>[\w-]+)/$',
        view=ProjectDetail.as_view(),
        name='projectDetail'
    ),

    url(
        regex=r'^(?P<project>\S+)/record/$',
        view=Record.as_view(),
        name='record'
    ),

    url(
        regex=r'^(?P<project>\S+)/record/start/$',
        view=start,
        name='recordStart'
    ),

    url(
        regex=r'^(?P<project>\S+)/record/(?P<recording>\S+)/upload/$',
        view=upload,
        name='recordUpload'
    ),

    url(
        regex=r'^(?P<project>\S+)/record/(?P<recording>\S+)/finish/$',
        view=finish,
        name='recordFinish'
    ),

    # url(
    #     regex=r'^view/(?P<email>\S+)/$',
    #     view=,
    #     name=''
    # ),
]

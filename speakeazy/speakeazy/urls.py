# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from speakeazy.speakeazy.views.createProject import CreateProject
from speakeazy.speakeazy.views.home import Home

urlpatterns = [
    url(
        regex=r'^home/$',
        view=Home.as_view(),
        name="home"
    ),

    url(
        regex=r'^create-project/$',
        view=CreateProject.as_view(),
        name="createProject"
    ),

    url(r'^projects/', include("speakeazy.speakeazy.views.projects.urls", namespace="projects")),
    url(r'^groups/(?P<group>\S+)/', include("speakeazy.speakeazy.views.projects.urls", namespace="groups")),
]

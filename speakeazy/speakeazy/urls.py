# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from speakeazy.speakeazy.views.home import Home
from speakeazy.speakeazy.views.newProject import NewProject

urlpatterns = [
    url(
        regex=r'^home/$',
        view=Home.as_view(),
        name="home"
    ),

    url(
        regex=r'^new-project/$',
        view=NewProject.as_view(),
        name="newProject"
    ),

    url(r'^projects/', include("speakeazy.speakeazy.views.projects.urls", namespace="projects")),
    url(r'^groups/(?P<group>\S+)/', include("speakeazy.speakeazy.views.projects.urls", namespace="groups")),
]

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from speakeazy.projects.views.home import Home
from speakeazy.projects.views.newProject import NewProject
from speakeazy.projects.views.projectList import ProjectList

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

    url(
        regex=r'^projects/$',
        view=ProjectList.as_view(),
        name="projectList"
    ),

    url(r'^projects/(?P<project>[\w-]+)/', include("speakeazy.projects.views.projects.urls", namespace="projects")),
]

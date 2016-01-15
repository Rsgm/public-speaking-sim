# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from speakeazy.projects.views.newProject import NewProject
from speakeazy.projects.views.projectList import ProjectList

urlpatterns = [
    url(
        regex=r'^new/$',
        view=NewProject.as_view(),
        name="newProject"
    ),

    url(
        regex=r'^$',
        view=ProjectList.as_view(),
        name="projectList"
    ),

    url(r'^p/(?P<project>[\w-]+)/', include("speakeazy.projects.views.project.urls", namespace="project")),
]

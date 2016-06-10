# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from speakeazy.projects.views.views import CreateProject, ProjectList

urlpatterns = [
    url(
        regex=r'^create/$',
        view=CreateProject.as_view(),
        name="create_project"
    ),

    url(
        regex=r'^$',
        view=ProjectList.as_view(),
        name="project_list"
    ),

    url(r'^p/(?P<project>[\w-]+)/', include("speakeazy.projects.views.user_project.urls", namespace="project")),
]

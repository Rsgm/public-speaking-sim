# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from speakeazy.speakeazy.views.groupHome import GroupHome
from speakeazy.speakeazy.views.groupList import GroupList
from speakeazy.speakeazy.views.home import Home
from speakeazy.speakeazy.views.newGroup import NewGroup
from speakeazy.speakeazy.views.newProject import NewProject
from speakeazy.speakeazy.views.projectList import ProjectList

urlpatterns = [
    url(
        regex=r'^home/$',
        view=Home.as_view(),
        name="home"
    ),

    url(
        regex=r'^group-home/$',
        view=GroupHome.as_view(),
        name="groupHome"
    ),

    url(
        regex=r'^new-project/$',
        view=NewProject.as_view(),
        name="newProject"
    ),

    url(
        regex=r'^new-group/$',
        view=NewGroup.as_view(),
        name="newGroup"
    ),

    url(
        regex=r'^groups/$',
        view=GroupList.as_view(),
        name="groupList"
    ),

    url(
        regex=r'^projects/$',
        view=ProjectList.as_view(),
        name="projectList"
    ),

    url(r'^projects/(?P<project>[\w-]+)/', include("speakeazy.speakeazy.views.projects.urls", namespace="projects")),
    url(r'^groups/(?P<group>\S+)/', include("speakeazy.speakeazy.views.groups.urls", namespace="groups")),
    url(r'^join/', include("speakeazy.speakeazy.views.join.urls", namespace="join")),
]

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from speakeazy.groups.views.groupDashboard import GroupDashboard
from speakeazy.groups.views.groupList import GroupList
from django.conf.urls import include, url
from speakeazy.groups.views.joinGroup import JoinGroup
from speakeazy.groups.views.newGroup import NewGroup

urlpatterns = [
    url(
        regex=r'^$',
        view=GroupList.as_view(),
        name="groupList"
    ),

    url(
        regex=r'^home$',
        view=GroupDashboard.as_view(),
        name="groupDashboard"
    ),

    url(
        regex=r'^new/$',
        view=NewGroup.as_view(),
        name="newGroup"
    ),

    url(
        regex=r'^join/$',
        view=JoinGroup.as_view(),
        name="joinGroup"
    ),

    url(r'^g/(?P<group>[\w-]+)/', include("speakeazy.groups.views.group.urls", namespace="group")),
]

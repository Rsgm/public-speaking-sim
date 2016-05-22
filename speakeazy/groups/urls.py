# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from speakeazy.groups.views.groupDashboard import GroupDashboard
from speakeazy.groups.views.groupList import GroupList
from django.conf.urls import include, url
from speakeazy.groups.views.joinGroup import JoinGroup, JoinGroupLink
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

    url(
        regex=r'^join/(?P<group>.+)/(?P<token>\w+)/$',
        view=JoinGroupLink.as_view(),
        name="join_group_link"
    ),

    url(r'^g/(?P<group>[\w-]+)/', include("speakeazy.groups.views.group.urls", namespace="group")),
]

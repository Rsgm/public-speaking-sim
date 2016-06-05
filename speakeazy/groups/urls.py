# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from speakeazy.groups.views.createGroup import CreateGroup
from speakeazy.groups.views.groupDashboard import GroupDashboard
from speakeazy.groups.views.groupList import GroupList
from speakeazy.groups.views.joinGroup import JoinGroup, JoinGroupLink

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
        regex=r'^create/$',
        view=CreateGroup.as_view(),
        name="create_group"
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

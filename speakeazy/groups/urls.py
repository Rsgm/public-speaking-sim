# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from speakeazy.groups.views.groupList import GroupList
from django.conf.urls import include, url
from speakeazy.groups.views.joinGroup import JoinGroup
from speakeazy.groups.views.newGroup import NewGroup

urlpatterns = [
    # url(
    #     regex=r'^home/$',
    #     view=GroupList.as_view(),
    #     name="groupList"
    # ),

    url(
        regex=r'^list/$',
        view=GroupList.as_view(),
        name="groupList"
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

    url(r'^group/(?P<group>[\w-]+)/', include("speakeazy.groups.views.group.urls", namespace="group")),
]

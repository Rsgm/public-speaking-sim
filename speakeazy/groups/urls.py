# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from speakeazy.groups.views.groupHome import GroupHome
from speakeazy.groups.views.groupList import GroupList

from django.conf.urls import include, url
from speakeazy.groups.views.newGroup import NewGroup

urlpatterns = [
    url(
        regex=r'^group-home/$',
        view=GroupHome.as_view(),
        name="groupHome"
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

    url(r'^groups/(?P<group>\S+)/', include("speakeazy.groups.views.groups.urls", namespace="groups")),
    url(r'^join/', include("speakeazy.groups.views.join.urls", namespace="join")),
]

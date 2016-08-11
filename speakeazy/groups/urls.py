# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from vanilla.views import TemplateView

from speakeazy.groups.views.createGroup import CreateGroup
from speakeazy.groups.views.admin import Admin
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
        regex=r'^home/$',
        view=RedirectView.as_view(pattern_name='groups:dashboard', permanent=True),
    ),

    url(
        regex=r'^dashboard$',
        view=GroupDashboard.as_view(),
        name="dashboard"
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

    url(
        regex=r'^admin$',
        view=Admin.as_view(),
        name="admin"
    ),
    url(
        regex=r'^admin/.*$',
        view=Admin.as_view(),
    ),

    url(r'^g/(?P<group>[\w-]+)/', include("speakeazy.groups.views.group.urls", namespace="group")),
]

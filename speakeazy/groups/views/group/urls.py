# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from speakeazy.groups.views.group.groupView import GroupView

urlpatterns = [
    # url(
    #     regex=r'^/admin$',
    #     view=GroupAdmin.as_view(),
    #     name='groupAdmin'
    # ),

    url(
        regex=r'^$',
        view=GroupView.as_view(),
        name='groupView'
    ),

    url(r'^audience/', include("speakeazy.groups.views.group.audience.urls", namespace="audience")),
    url(r'^invite/', include("speakeazy.groups.views.group.invite.urls", namespace="invite")),
    url(r'^user/', include("speakeazy.groups.views.group.user.urls", namespace="user")),
]

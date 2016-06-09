# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from speakeazy.groups.views.group.groupView import GroupView

urlpatterns = [
    url(
        regex=r'^$',
        view=GroupView.as_view(),
        name='groupView'
    ),

    url(r'^audiences/', include("speakeazy.groups.views.group.audience.urls", namespace="audience")),
    url(r'^submissions/', include("speakeazy.groups.views.group.submission.urls", namespace="submission")),

    url(r'^invites/', include("speakeazy.groups.views.group.manage.invite.urls", namespace="invite")),
    url(r'^users/', include("speakeazy.groups.views.group.manage.user.urls", namespace="user")),
    # url(r'^manage/', include("speakeazy.groups.views.group.submission.urls", namespace="submission")),
]

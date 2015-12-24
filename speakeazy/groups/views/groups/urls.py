# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

urlpatterns = [
    # url(
    #     regex=r'^/admin$',
    #     view=GroupAdmin.as_view(),
    #     name='groupAdmin'
    # ),

    url(r'^audience/', include("speakeazy.groups.views.groups.audience.urls", namespace="audience")),
    url(r'^invite/', include("speakeazy.groups.views.groups.invite.urls", namespace="invite")),
    url(r'^user/', include("speakeazy.groups.views.groups.user.urls", namespace="user")),
]

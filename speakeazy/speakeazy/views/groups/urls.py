# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from speakeazy.speakeazy.views.groups.home import Home

urlpatterns = [
    # url(
    #     regex=r'^/admin$',
    #     view=GroupAdmin.as_view(),
    #     name='groupAdmin'
    # ),

    url(r'^audience/', include("speakeazy.speakeazy.views.groups.audience.urls", namespace="audience")),
    url(r'^invite/', include("speakeazy.speakeazy.views.groups.invite.urls", namespace="invite")),
    url(r'^user/', include("speakeazy.speakeazy.views.groups.user.urls", namespace="user")),
]

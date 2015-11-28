# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from speakeazy.speakeazy.views.groups.home import Home

urlpatterns = [
    url(
        regex=r'^$',
        view=Home.as_view(),
        name='home'
    ),

    url(r'^admin/', include("speakeazy.speakeazy.views.groups.admin.urls", namespace="admin")),

    # url(
    #     regex=r'^submissions/$',
    #     view=,
    #     name=
    # ),
    #
    # url(
    #     regex=r'^submissions/(?P<submission>)$',
    #     view=,
    #     name=
    # ),
]

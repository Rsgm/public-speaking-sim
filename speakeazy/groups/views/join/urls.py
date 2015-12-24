# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from speakeazy.groups.views.join.views import Home, Token, Name, Request

from django.conf.urls import url

urlpatterns = [
    url(
        regex=r'^/$',
        view=Home.as_view(),
        name='home'
    ),

    url(
        regex=r'^token/$',
        view=Token.as_view(),
        name='token'
    ),

    url(
        regex=r'^name/$',
        view=Name.as_view(),
        name='name'
    ),

    url(
        regex=r'^request/$',
        view=Request.as_view(),
        name='request'
    ),
]

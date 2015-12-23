# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.speakeazy.views.groups.user.views import ListUsers, ViewUser, UpdateUser, DeleteUser
from speakeazy.speakeazy.views.join.views import Home, Token, Name, Request

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

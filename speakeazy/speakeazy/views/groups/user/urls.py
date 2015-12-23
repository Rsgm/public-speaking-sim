# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.speakeazy.views.groups.user.views import ListUsers, ViewUser, UpdateUser, DeleteUser

urlpatterns = [
    url(
        regex=r'^list/$',
        view=ListUsers.as_view(),
        name='list'
    ),

    url(
        regex=r'^view/(?P<user>[\w-]+)/$',
        view=ViewUser.as_view(),
        name='view'
    ),

    url(
        regex=r'^update/(?P<user>[\w-]+)/$',
        view=UpdateUser.as_view(),
        name='update'
    ),

    url(
        regex=r'^delete/(?P<user>[\w-]+)/$',
        view=DeleteUser.as_view(),
        name='delete'
    ),
]

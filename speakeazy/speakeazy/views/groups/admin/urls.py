# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.speakeazy.views.groups.admin.addUser import AddUser
from speakeazy.speakeazy.views.groups.admin.create import Create
from speakeazy.speakeazy.views.groups.admin.home import Home
from speakeazy.speakeazy.views.groups.admin.removeUser import RemoveUser
from speakeazy.speakeazy.views.groups.admin.updateUse import UpdateUser

urlpatterns = [
    url(
        regex=r'^/$',
        view=Home.as_view(),
        name='home'
    ),

    url(
        regex=r'^create/$',
        view=Create.as_view(),
        name='createGroup'
    ),

    url(
        regex=r'^add/$',
        view=AddUser.as_view(),
        name='addUser'
    ),

    url(
        regex=r'^update/(?P<user>\S+)$',
        view=UpdateUser.as_view(),
        name='updateUser'
    ),

    url(
        regex=r'^remove/(?P<user>\S+)$',
        view=RemoveUser.as_view(),
        name='updateUser'
    ),
]

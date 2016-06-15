# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from speakeazy.groups.views.group.manage.user.views import List, View, Update, Delete

urlpatterns = [
    url(
        regex=r'^$',
        view=List.as_view(),
        name='list'
    ),

    url(
        regex=r'^view/(?P<user>[\w-]+)/$',
        view=View.as_view(),
        name='view'
    ),

    url(
        regex=r'^update/(?P<user>[\w-]+)/$',
        view=Update.as_view(),
        name='update'
    ),

    url(
        regex=r'^delete/(?P<user>[\w-]+)/$',
        view=Delete.as_view(),
        name='delete'
    ),
]

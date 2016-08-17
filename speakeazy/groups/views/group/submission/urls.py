# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.groups.views.group.submission.views import List, View, Update, Delete

urlpatterns = [
    url(
        regex=r'^$',
        view=List.as_view(),
        name='list'
    ),

    url(
        regex=r'^(?P<pk>[\d]+)/$',
        view=View.as_view(),
        name='view'
    ),

    url(
        regex=r'^(?P<pk>[\d]+)/update/$',
        view=Update.as_view(),
        name='update'
    ),

    url(
        regex=r'^(?P<pk>[\d]+)/delete/$',
        view=Delete.as_view(),
        name='delete'
    ),
]

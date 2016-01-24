# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from speakeazy.groups.views.group.submission.views import List, View, Update, Delete, Add, Evaluate

from django.conf.urls import url

urlpatterns = [
    url(
        regex=r'^list/$',
        view=List.as_view(),
        name='list'
    ),

    url(
        regex=r'^view/(?P<submission>[\w-]+)/$',
        view=View.as_view(),
        name='view'
    ),

    url(
        regex=r'^add/$',
        view=Add.as_view(),
        name='add'
    ),

    url(
        regex=r'^update/(?P<submission>[\w-]+)/$',
        view=Update.as_view(),
        name='update'
    ),

    url(
        regex=r'^delete/(?P<submission>[\w-]+)/$',
        view=Delete.as_view(),
        name='delete'
    ),

    url(
        regex=r'^evaluate/(?P<submission>[\w-]+)/$',
        view=Evaluate.as_view(),
        name='evaluate'
    ),
]

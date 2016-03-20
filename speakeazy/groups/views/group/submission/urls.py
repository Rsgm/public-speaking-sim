# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.groups.views.group.submission.views import List, View, Delete, Evaluate, Request

urlpatterns = [
    url(
        regex=r'^$',
        view=List.as_view(),
        name='list'
    ),

    url(
        regex=r'^view/(?P<pk>[\w-]+)/$',
        view=View.as_view(),
        name='view'
    ),

    # url(
    #     regex=r'^add/$',
    #     view=Add.as_view(),
    #     name='add'
    # ),

    # url(
    #     regex=r'^update/(?P<pk>[\w-]+)/$',
    #     view=Update.as_view(),
    #     name='update'
    # ),

    url(
        regex=r'^delete/(?P<pk>[\w-]+)/$',
        view=Delete.as_view(),
        name='delete'
    ),

    url(
        regex=r'^evaluate/(?P<pk>[\w-]+)/$',
        view=Evaluate.as_view(),
        name='evaluate'
    ),

    url(
        regex=r'^request/(?P<pk>[\w-]+)/$',
        view=Request.as_view(),
        name='request'
    ),
]

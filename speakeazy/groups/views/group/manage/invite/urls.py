# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from speakeazy.groups.views.group.manage.invite.views import List, View, Update, Delete, Add

urlpatterns = [
    url(
        regex=r'^$',
        view=List.as_view(),
        name='list'
    ),

    url(
        regex=r'^view/(?P<invite>[\w-]+)/$',
        view=View.as_view(),
        name='view'
    ),

    url(
        regex=r'^add/$',
        view=Add.as_view(),
        name='add'
    ),

    url(
        regex=r'^update/(?P<invite>[\w-]+)/$',
        view=Update.as_view(),
        name='update'
    ),

    url(
        regex=r'^delete/(?P<invite>[\w-]+)/$',
        view=Delete.as_view(),
        name='delete'
    ),
]

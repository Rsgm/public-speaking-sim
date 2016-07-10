# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from speakeazy.projects.views.user_project.views import View, Delete, Update

urlpatterns = [
    url(
        regex=r'^$',
        view=View.as_view(),
        name='projectView'
    ),

    url(
        regex=r'^update/$',
        view=Update.as_view(),
        name='update'
    ),

    url(
        regex=r'^delete/$',
        view=Delete.as_view(),
        name='delete'
    ),
]

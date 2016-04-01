# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.recordings.views.recording.share.views import CreateSharedUser, CreateSharedLink

urlpatterns = [
    url(
        regex=r'^user/$',
        view=CreateSharedUser.as_view(),
        name='user'
    ),
    # url(
    #     regex=r'^submission$',
    #     view=View.as_view(),
    #     name='user'
    # ),
    # url(
    #     regex=r'^user$',
    #     view=CreateSharedLink.as_view(),
    #     name='link'
    # ),
    # url(
    #     regex=r'^list$',
    #     view=CreateSharedLink.as_view(),
    #     name='link'
    # )
]

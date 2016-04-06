# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from speakeazy.recordings.views.recording.share.views import CreateSharedUser, CreateSharedLink, CreateGroupSubmission

urlpatterns = [
    # url(
    #     regex=r'^user/$',
    #     view=CreateSharedUser.as_view(),
    #     name='user'
    # ),
    # url(
    #     regex=r'^list$',
    #     view=CreateSharedLink.as_view(),
    #     name='link'
    # )

    url(
        regex=r'^submission/$',
        view=CreateGroupSubmission.as_view(),
        name='submission'
    ),
]

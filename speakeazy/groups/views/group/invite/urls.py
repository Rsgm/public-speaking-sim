# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from speakeazy.groups.views.group.invite.views import ViewInvite, ListInvites

from django.conf.urls import url

urlpatterns = [
    url(
        regex=r'^List/$',
        view=ListInvites.as_view(),
        name='list'
    ),
    #
    # url(
    #     regex=r'^create/$',
    #     view=AddInvite.as_view(),
    #     name='add'
    # ),

    url(
        regex=r'^view/(?P<slug>[\w-]+)/$',
        view=ViewInvite.as_view(),
        name='view'
    ),

    # url(
    #     regex=r'^delete/(?P<slug>[\w-]+)/$',
    #     view=DeleteInvite.as_view(),
    #     name='delete'
    # ),
]

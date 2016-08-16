# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from speakeazy.groups.views.group.dashboard import Dashboard

urlpatterns = [
    url(
        regex=r'^$',
        view=Dashboard.as_view(),
        name='dashboard'
    ),

    url(r'^audiences/', include("speakeazy.groups.views.group.audience.urls", namespace="audience")),
    url(r'^submissions/', include("speakeazy.groups.views.group.submission.urls", namespace="submission")),
]

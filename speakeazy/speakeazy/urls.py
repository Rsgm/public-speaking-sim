# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from speakeazy.speakeazy.views import Dashboard

urlpatterns = [
    url(
        regex=r'^dashboard/$',
        view=Dashboard.as_view(),
        name="dashboard"
    ),
]

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from speakeazy.speakeazy.views import Home

urlpatterns = [
    url(
        regex=r'^home/$',
        view=Home.as_view(),
        name="home"
    )
]

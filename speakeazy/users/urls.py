# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from speakeazy.speakeazy.views import Dashboard

urlpatterns = [
    url(
        regex=r'^account/signup/$',
        view=RedirectView.as_view(pattern_name='userena_signup', permanent=True)
    ),

    url(
        regex=r'^account/register/$',
        view='userena.views.signup',
        name='userena_signup'
    ),

    url(
        regex=r'^account/activate/(?P<activation_key>\w+)/$',
        view='userena.views.activate',
        kwargs={'success_url': 'speakeazy:dashboard'},
        name='userena_activate'
    ),
]

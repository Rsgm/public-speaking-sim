# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from speakeazy.speakeazy.views import Dashboard
from speakeazy.users.forms import SpeakeazySignupForm

urlpatterns = [
    url(
        r'^register/$',
        'userena.views.signup',
        {'signup_form': SpeakeazySignupForm},
        'userena_register'
    ),

    url(
        regex=r'^signup/$',
        view=RedirectView.as_view(pattern_name='userena_register', permanent=True)
    ),

    url(
        regex=r'^activate/(?P<activation_key>\w+)/$',
        view='userena.views.activate',
        kwargs={'success_url': 'speakeazy:dashboard'},
        name='userena_activate'
    ),
]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from speakeazy.users.forms import SpeakeazySignupForm

urlpatterns = [
                  url(r'^$', TemplateView.as_view(template_name='speakeazy/landing.html'), name="home"),

                  # Django Admin, use {% url 'admin:index' %}
                  url(settings.ADMIN_URL + 'docs/', include('django.contrib.admindocs.urls')),
                  url(settings.ADMIN_URL, include(admin.site.urls)),
                  url(r'^hijack/', include('hijack.urls')),

                  # User management
                  url(r'^account/signup/$', 'userena.views.signup', {'signup_form': SpeakeazySignupForm},
                      name='userena_signup'),
                  url(r'^account/activate/(?P<activation_key>\w+)/$', 'userena.views.activate',
                      {'success_url': 'speakeazy:dashboard'}, name='userena_activate'),
                  url(r'^account/', include('userena.urls')),

                  # Your stuff: custom urls includes go here
                  url(r'', include("speakeazy.speakeazy.urls", namespace="speakeazy")),
                  url(r'^projects/', include("speakeazy.projects.urls", namespace="projects")),
                  url(r'^groups/', include("speakeazy.groups.urls", namespace="groups")),
                  url(r'^recordings/', include("speakeazy.recordings.urls", namespace="recordings")),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request),
        url(r'^403/$', default_views.permission_denied),
        url(r'^404/$', default_views.page_not_found),
        url(r'^500/$', default_views.server_error),
    ]

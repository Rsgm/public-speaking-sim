# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from speakeazy.groups.models import Project

from braces.views import LoginRequiredMixin
from django.views.generic.list import ListView


class UserList(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'speakeazy/projects/project_view.html'

    # These next two lines tell the view to index lookups by project
    slug_field = "project"
    slug_url_kwarg = "project"

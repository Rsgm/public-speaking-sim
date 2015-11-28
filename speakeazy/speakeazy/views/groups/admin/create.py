# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from braces.views import LoginRequiredMixin
from speakeazy.speakeazy.models import Project
from vanilla.model_views import CreateView
from vanilla.views import TemplateView


class Create(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'speakeazy/groups/admin/home.html'

    # These next two lines tell the view to index lookups by project
    slug_field = "project"
    slug_url_kwarg = "project"

    # if parent group is empty, set group to speakeazy

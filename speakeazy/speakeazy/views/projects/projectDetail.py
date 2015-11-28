# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from braces.views import LoginRequiredMixin
from speakeazy.speakeazy.models import Project
from vanilla.model_views import DetailView


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'speakeazy/projects/project_detail.html'

    # These next two lines tell the view to index lookups by project
    lookup_field = 'slug'
    lookup_url_kwarg = 'project'

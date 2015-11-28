# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from speakeazy.speakeazy.models import Project
from vanilla.views import TemplateView


class Home(LoginRequiredMixin, TemplateView):
    model = Project
    template_name = 'speakeazy/groups/admin/home.html'

    # These next two lines tell the view to index lookups by project
    slug_field = "project"
    slug_url_kwarg = "project"

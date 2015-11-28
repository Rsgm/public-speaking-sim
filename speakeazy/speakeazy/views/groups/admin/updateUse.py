# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from speakeazy.speakeazy.models import Project, GroupRole
from vanilla.model_views import CreateView, UpdateView
from vanilla.views import TemplateView


class UpdateUser(LoginRequiredMixin, UpdateView):
    model = GroupRole
    template_name = 'speakeazy/groups/admin/update_user.html'

    # These next two lines tell the view to index lookups by project
    slug_field = "project"
    slug_url_kwarg = "project"

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from speakeazy.projects.models import UserProject

from braces.views import LoginRequiredMixin
from vanilla.model_views import ListView


class ProjectList(LoginRequiredMixin, ListView):
    model = UserProject
    template_name = 'projects/project_list.html'

    def get_queryset(self):
        return UserProject.objects.filter(user=self.request.user).order_by('-due_date')

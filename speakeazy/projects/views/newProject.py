# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from speakeazy.groups.models import Audience
from speakeazy.projects.forms import NewProjectForm
from vanilla.model_views import CreateView


class NewProject(LoginRequiredMixin, CreateView):
    template_name = 'projects/new_project.html'

    def get_form(self, data=None, files=None, **kwargs):
        user = self.request.user

        group_list = user.group_set.values_list('id', flat=True)
        audiences = Audience.objects.filter(group__in=group_list)

        return NewProjectForm(user, audiences, data=data, files=files)

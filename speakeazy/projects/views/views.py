# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from vanilla import ListView

from speakeazy.groups.models import Audience
from speakeazy.projects.forms import CreateUserProjectForm
from vanilla.model_views import CreateView

from speakeazy.projects.models import UserProject


class CreateProject(LoginRequiredMixin, CreateView):
    template_name = 'projects/create_project.html'

    def get_form(self, data=None, files=None, **kwargs):
        user = self.request.user

        group_list = user.group_set.values_list('id', flat=True)
        audiences = Audience.objects.filter(group__in=group_list, file_webm__isnull=False)

        return CreateUserProjectForm(user, audiences, data=data, files=files)


class ProjectList(LoginRequiredMixin, ListView):
    model = UserProject
    template_name = 'projects/project_list.html'

    def get_queryset(self):
        return UserProject.objects.filter(user=self.request.user).order_by('-due_date')

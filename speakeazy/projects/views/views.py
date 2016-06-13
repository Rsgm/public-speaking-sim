# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from vanilla import ListView
from vanilla.model_views import CreateView

from speakeazy.projects.forms import CreateUserProjectForm, CreatePracticeProjectForm
from speakeazy.projects.models import UserProject


class CreateProject(LoginRequiredMixin, CreateView):
    template_name = 'projects/create_project.html'

    def get_form(self, data=None, files=None, **kwargs):
        return CreateUserProjectForm(self.request.user, data=data, files=files)


class MagicHat(LoginRequiredMixin, CreateView):
    """
    Create practice projects, or magic hat
    Creates a practice project using the create practice project form
    """
    template_name = 'projects/magic_hat.html'

    def get_form(self, data=None, files=None, **kwargs):
        return CreatePracticeProjectForm(user=self.request.user, data=data, files=files, **kwargs)


class ProjectList(LoginRequiredMixin, ListView):
    model = UserProject
    template_name = 'projects/project_list.html'

    def get_queryset(self):
        return UserProject.objects.filter(user=self.request.user).order_by('-due_date')

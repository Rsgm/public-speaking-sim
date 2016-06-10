# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from vanilla.model_views import UpdateView, DeleteView

from speakeazy.projects.forms import UserProjectForm
from speakeazy.projects.models import UserProject, Recording
from speakeazy.recordings.models import RECORDING_FINISHED
from vanilla.views import TemplateView


class View(LoginRequiredMixin, TemplateView):
    model = UserProject
    template_name = 'projects/project/view.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        kwargs['project'] = get_object_or_404(
            UserProject.objects.filter(user=self.request.user, slug=self.kwargs['project']))
        kwargs['recording_list'] = Recording.objects.filter(project=kwargs['project'], state=RECORDING_FINISHED)

        return kwargs


class Update(LoginRequiredMixin, UpdateView):
    model = UserProject
    fields = ['description', 'due_date']
    template_name = 'projects/project/update.html'

    def get_object(self):
        return get_object_or_404(UserProject.objects.filter(user=self.request.user, slug=self.kwargs['project']))

    def get_form(self, data=None, files=None, **kwargs):
        return UserProjectForm(self.request.user, data=data, files=files, **kwargs)


class Delete(LoginRequiredMixin, DeleteView):
    model = UserProject
    template_name = 'projects/project/delete.html'

    def get_object(self):
        return get_object_or_404(UserProject.objects.filter(user=self.request.user, slug=self.kwargs['project']))

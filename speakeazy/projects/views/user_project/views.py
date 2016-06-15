# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models.query import Prefetch
from django.shortcuts import get_object_or_404
from vanilla.model_views import UpdateView, DeleteView, DetailView

from speakeazy.projects.models import UserProject, Recording
from speakeazy.projects.views.user_project.forms import UserProjectForm
from speakeazy.recordings.models import RECORDING_FINISHED


class View(LoginRequiredMixin, DetailView):
    model = UserProject
    template_name = 'projects/project/view.html'

    def get_object(self):
        queryset = UserProject.objects.filter(user=self.request.user, slug=self.kwargs['project']) \
            .select_related('practiceproject', 'practiceproject__practice_speech') \
            .prefetch_related(Prefetch('recording_set',
                                       to_attr='recordings',
                                       queryset=Recording.objects.filter(
                                           state=RECORDING_FINISHED)
                                       ))

        return get_object_or_404(queryset)


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
    success_url = reverse_lazy('projects:project_list')

    def get_object(self):
        return get_object_or_404(UserProject.objects.filter(user=self.request.user, slug=self.kwargs['project']))

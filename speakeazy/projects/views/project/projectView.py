# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from speakeazy.projects.models import Project, Recording
from speakeazy.recordings.models import FINISHED
from vanilla.views import TemplateView


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/project/project_view.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        kwargs['project'] = get_object_or_404(
            Project.objects.filter(user=self.request.user, slug=self.kwargs['project']))
        kwargs['recording_list'] = Recording.objects.filter(project=kwargs['project'], state=FINISHED)

        return kwargs

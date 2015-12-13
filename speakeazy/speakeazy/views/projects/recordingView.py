# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from speakeazy.speakeazy.models import Project, Recording
from vanilla.model_views import DetailView
from vanilla.views import TemplateView


class RecordingView(LoginRequiredMixin, TemplateView):
    template_name = 'speakeazy/projects/recording_view.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        kwargs['recording'] = get_object_or_404(
            Recording.objects.filter(project__user=self.request.user, project__slug=self.kwargs['project'],
                                     slug=self.kwargs['recording']))

        return kwargs

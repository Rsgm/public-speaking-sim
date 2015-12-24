# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from speakeazy.projects.models import Project

from braces.views import LoginRequiredMixin
from speakeazy.recordings.models import Recording, FINISHED
from vanilla.views import TemplateView


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'speakeazy/home.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        kwargs['project_list'] = Project.objects.filter(user=self.request.user).order_by('-due_date')[:5]
        kwargs['recording_list'] = Recording.objects.filter(project__user=self.request.user, state=FINISHED).order_by(
            '-finish_time')[:5]
        return kwargs

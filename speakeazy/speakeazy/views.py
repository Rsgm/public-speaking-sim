# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from speakeazy.groups.models import Group

from speakeazy.projects.models import Project

from braces.views import LoginRequiredMixin
from speakeazy.recordings.models import Recording, RECORDING_FINISHED
from vanilla.views import TemplateView


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'speakeazy/dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        projects = Project.objects.filter(user=self.request.user)

        kwargs['project_recent_list'] = projects.order_by('-created_time')[:6]
        kwargs['project_due_list'] = projects.order_by('-due_date')[:6]
        kwargs['project_list'] = Project.objects.filter(user=self.request.user).order_by('-due_date')[:6]
        kwargs['recording_list'] = Recording.objects.filter(project__user=self.request.user,
                                                            state=RECORDING_FINISHED).order_by('-finish_time')[:6]

        kwargs['group_list'] = Group.objects.filter(groupmembership__user=self.request.user).order_by('-created_time')

        return kwargs

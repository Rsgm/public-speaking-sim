# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from speakeazy.groups.models import Group

from speakeazy.projects.models import UserProject

from braces.views import LoginRequiredMixin
from speakeazy.recordings.models import Recording, RECORDING_FINISHED
from vanilla.views import TemplateView


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'speakeazy/dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        projects = UserProject.objects.filter(user=self.request.user)

        kwargs['project_list'] = projects.order_by('-created_time')[:8]
        kwargs['recording_list'] = Recording.objects.filter(project__user=self.request.user,
                                                            state=RECORDING_FINISHED).order_by('-finish_time')[:8]

        kwargs['group_list'] = Group.objects.filter(groupmembership__user=self.request.user).order_by('-created_time')

        return kwargs

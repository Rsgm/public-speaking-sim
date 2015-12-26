# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from vanilla.views import TemplateView


class GroupHome(LoginRequiredMixin, TemplateView):
    template_name = 'groups/group_home.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self
        #
        # kwargs['project_list'] = Project.objects.filter(user=self.request.user).order_by('-due_date')[:5]
        # kwargs['recording_list'] = Recording.objects.filter(project__user=self.request.user, state=FINISHED).order_by(
        #     '-finish_time')[:5]
        return kwargs

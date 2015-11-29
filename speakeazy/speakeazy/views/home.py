# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from braces.views import LoginRequiredMixin
from ratelimit.decorators import ratelimit
from ratelimit.mixins import RatelimitMixin
from speakeazy.speakeazy.models import Project
from vanilla.views import TemplateView


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'speakeazy/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        context['project_list'] = Project.objects.filter(user=self.request.user).order_by('due_date').reverse()[:5]
        return context

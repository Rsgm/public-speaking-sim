# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from speakeazy.speakeazy.models import Project, Audience
from vanilla.model_views import CreateView


class CreateProject(LoginRequiredMixin, CreateView):
    template_name = 'speakeazy/create_project.html'
    model = Project

    fields = ['name', 'description', 'due_date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.audience = Audience.objects.first()
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

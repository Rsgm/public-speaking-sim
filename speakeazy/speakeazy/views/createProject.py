# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from speakeazy.speakeazy.forms.project import ProjectCreate
from speakeazy.speakeazy.models import Project
from vanilla.model_views import CreateView


class CreateProject(LoginRequiredMixin, CreateView):
    template_name = 'speakeazy/create_project.html'
    model = Project

    def get_form(self, *args, **kwargs):
        return ProjectCreate(kwargs['user'])

    def get(self, request, *args, **kwargs):
        form = self.get_form(user=request.user)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        self.object.user = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

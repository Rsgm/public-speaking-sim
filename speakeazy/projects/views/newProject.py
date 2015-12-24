# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from speakeazy.projects.forms.projectForms import ProjectCreate
from speakeazy.projects.models import Project, Audience

from braces.views import LoginRequiredMixin
from vanilla.views import FormView


class NewProject(LoginRequiredMixin, FormView):
    template_name = 'speakeazy/create_project.html'
    project = None

    def get_form(self, user=None, data=None, files=None, **kwargs):
        group_list = user.group_set.values_list('id', flat=True)
        audiences = Audience.objects.filter(group__in=group_list)
        return ProjectCreate(audiences, data)

    def get(self, request, *args, **kwargs):
        form = self.get_form(user=request.user)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(user=request.user, data=request.POST)
        if form.is_valid():
            self.project = Project()
            self.project.user = request.user
            self.project.name = form.data['name']
            self.project.description = form.data['description']
            self.project.audience = Audience.objects.get(pk=form.data['audience'])
            self.project.due_date = form.data['due_date']
            self.project.save()

            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return self.project.get_absolute_url()

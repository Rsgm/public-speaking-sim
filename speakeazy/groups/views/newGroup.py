# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.http.response import HttpResponseRedirect
from speakeazy.groups.models import Group, GroupMembership, Authorization
from braces.views import LoginRequiredMixin
from speakeazy.groups.views.forms import NewGroupForm
from vanilla.model_views import CreateView


class NewGroup(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['name', 'description', 'logo']
    template_name = 'groups/new_group.html'

    def get_form(self, data=None, files=None, **kwargs):
        user = self.request.user
        return NewGroupForm(user, data=data, files=files, **kwargs)

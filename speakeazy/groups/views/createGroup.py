# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from speakeazy.groups.models import Group, DefaultGroupStructure, DefaultGroupRole
from speakeazy.groups.views.forms import CreateGroupForm
from vanilla.model_views import CreateView


class CreateGroup(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'groups/create_group.html'

    def get_form(self, data=None, files=None, **kwargs):
        return CreateGroupForm(self.request.user, data=data, files=files, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        structures = DefaultGroupStructure.objects.prefetch_related('default_role_types')
        kwargs['structures'] = [{'id': s.pk, 'name': s.name, 'description': s.description,
                                 'list': s.default_role_types.values_list('name', flat=True)} for s in structures]

        roles = DefaultGroupRole.objects.prefetch_related('permissions')
        kwargs['roles'] = [{'id': r.pk, 'name': r.name, 'description': r.description,
                            'list': r.permissions.values_list('name', flat=True)} for r in roles]

        return kwargs

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from speakeazy.groups.models import Group
from speakeazy.groups.views.forms import CreateGroupForm, DefaultStructureForm, DefaultRolesForm
from vanilla.views import TemplateView


class CreateGroup(LoginRequiredMixin, TemplateView):
    model = Group
    template_name = 'groups/create_group.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        kwargs['group_form'] = CreateGroupForm(self.request.user)
        kwargs['structure_form'] = DefaultStructureForm()
        kwargs['roles_form'] = DefaultRolesForm()

        # structures = DefaultGroupStructure.objects.prefetch_related('default_role_types')
        # kwargs['structures'] = [{'id': s.pk, 'name': s.name, 'description': s.description,
        #                          'list': s.default_role_types.values_list('name', flat=True)} for s in structures]
        #
        # kwargs['roles'] = DefaultGroupRole.objects.values('id', 'name', 'description')

        return kwargs

    def post(self, request, *args, **kwargs):
        group_form_class = CreateGroupForm
        structure_form_class = DefaultStructureForm
        roles_form_class = DefaultRolesForm

        group_form = group_form_class(request.user, data=request.POST, files=request.FILES)
        structure_form = structure_form_class(data=request.POST, files=request.FILES)
        roles_form = roles_form_class(data=request.POST, files=request.FILES)

        # validate group
        if group_form.is_valid():
            group, membership = group_form.save()
        else:
            return self.form_invalid(group_form)

        # validate structure
        if structure_form.is_valid():
            structure = structure_form.save(group, membership)
        else:
            group.delete()
            return self.form_invalid(structure_form)

        # validate roles, if no structure was picked
        if not structure:
            if roles_form.is_valid(structure):
                roles_form.save(group, membership)
            else:
                group.delete()
                return self.form_invalid(roles_form)

        return reverse_lazy('groups:group:groupView', kwargs={'group': group.slug})

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

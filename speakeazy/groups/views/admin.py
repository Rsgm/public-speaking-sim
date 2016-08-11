# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect

from speakeazy.groups.models import Group
from speakeazy.groups.views.forms import CreateGroupForm, DefaultStructureForm, DefaultRolesForm
from vanilla.views import TemplateView


class Admin(LoginRequiredMixin, TemplateView):
    template_name = 'groups/admin.html'

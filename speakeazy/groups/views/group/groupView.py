# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


from braces.views import LoginRequiredMixin
from vanilla.views import TemplateView


class GroupView(LoginRequiredMixin, TemplateView):
    template_name = 'groups/group/group_view.html'

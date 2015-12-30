# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin
from speakeazy.groups.views.forms import JoinForm


class JoinGroup(LoginRequiredMixin, FormView):
    template_name = 'groups/join_group.html'

    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        user = None

        if self.request.method in ('POST', 'PUT'):
            user = self.request.user

        return JoinForm(user, **kwargs)

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('groups:group:groupView', kwargs={'group': form.membership.group.name}))

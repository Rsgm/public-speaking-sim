# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin
from speakeazy.groups.models import GroupInvite, GroupMembership
from speakeazy.groups.views.forms import JoinForm


class JoinGroup(LoginRequiredMixin, FormView):
    template_name = 'groups/join_group.html'
    form_class = JoinForm

    def form_valid(self, form):
        user = self.request.user
        invite = form.invite

        if invite.uses and invite.uses > 0:
            # subtract from uses
            invite.uses -= 1
            invite.save()

        membership_queryset = GroupMembership.objects.filter(group=invite.group, user=user)

        # check for existing membership
        if membership_queryset.count() == 0:
            # create membership if none exists
            membership = GroupMembership(group=invite.group, user=user)
            membership.save()
            membership.authorizations.add(*invite.authorizations.all())
        else:
            # add authorizations to existing memberships
            membership = membership_queryset.get()
            membership.authorizations.add(*invite.authorizations.all())

        membership.save()

        return HttpResponseRedirect(reverse('groups:group:groupView', kwargs={'group': membership.group.slug}))

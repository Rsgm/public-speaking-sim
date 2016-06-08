# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from speakeazy.groups.mixins import GroupMixin
from speakeazy.groups.models import GroupMembership, GroupInvite, Submission
from speakeazy.groups.permissions import LIST_SUBMISSION, LIST_INVITE, LIST_USER
from vanilla.views import TemplateView


class GroupView(LoginRequiredMixin, GroupMixin, TemplateView):
    template_name = 'groups/group/group_view.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self
        kwargs['group'] = self.group

        if LIST_SUBMISSION in self.permissions:
            kwargs['submission_list'] = Submission.objects.filter(group=self.group).order_by('-created_time')[:6]

        if LIST_INVITE in self.permissions:
            kwargs['invite_list'] = GroupInvite.objects.filter(group=self.group).order_by('-created_time')[:6]

        if LIST_USER in self.permissions:
            kwargs['user_list'] = GroupMembership.objects.filter(group=self.group).order_by('-created_time')[:6]

        return kwargs

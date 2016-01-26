# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.db.models.aggregates import Count
from speakeazy.groups.mixins import LIST_SUBMISSION, GroupPermissiondMixin, LIST_USER, LIST_INVITE
from speakeazy.groups.models import Group, GroupMembership, Permission, GroupInvite, Submission
from speakeazy.recordings.models import Recording
from vanilla.views import TemplateView


class GroupView(LoginRequiredMixin, GroupPermissiondMixin, TemplateView):
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

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.db.models.aggregates import Count
from django.db.models.query import Prefetch

from speakeazy.groups.mixins import GroupMixin
from speakeazy.groups.models import GroupMembership, GroupInvite, Submission, Role
from speakeazy.groups.permissions import LIST_SUBMISSION, LIST_INVITE, LIST_USER
from vanilla.views import TemplateView


class Dashboard(LoginRequiredMixin, GroupMixin, TemplateView):
    template_name = 'groups/group/dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self
        kwargs['group'] = self.group

        if LIST_SUBMISSION in self.permissions:
            kwargs['submission_list'] = Submission.objects \
                                            .filter(group=self.group) \
                                            .select_related('recording', 'recording__project',
                                                            'recording__project__user') \
                                            .order_by('created_time')[:10]

        if LIST_INVITE in self.permissions:
            kwargs['invite_list'] = GroupInvite.objects \
                                        .filter(group=self.group) \
                                        .order_by('-created_time')[:10]

        if LIST_USER in self.permissions:
            kwargs['user_list'] = GroupMembership.objects \
                                      .filter(group=self.group) \
                                      .select_related('user') \
                                      .prefetch_related(Prefetch('roles',
                                                                 queryset=Role.objects.filter(group=self.group))) \
                                      .annotate(Count('roles__permissions')) \
                                      .order_by('-roles__permissions__count', 'user__username')[:10]

        return kwargs

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.db.models.aggregates import Count
from speakeazy.groups.permissions import LIST_SUBMISSION
from vanilla.views import TemplateView


class GroupDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'groups/group_dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        # group_memberships = GroupMembership.objects.filter(user=self.request.user)
        group_memberships = self.request.user.groupmembership_set
        # groups = group_memberships.values_list('group', flat=True)

        # kwargs['group_list'] = groups.order_by('-created_time')

        kwargs['recently_joined_list'] = group_memberships.select_related('group').order_by('-created_time')[:6]

        # list all groups with submissions that you have permission to list
        kwargs['groups_with_submission_list'] = group_memberships \
                                                    .filter(roles__permissions__name=LIST_SUBMISSION) \
                                                    .select_related('group') \
                                                    .annotate(submission_count=Count('group__submission')) \
                                                    .order_by('-submission_count')[:6]

        return kwargs

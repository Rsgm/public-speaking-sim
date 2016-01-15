# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.db.models.aggregates import Count
from speakeazy.groups.mixins import LIST_SUBMISSION
from speakeazy.groups.models import Group, GroupMembership
from speakeazy.recordings.models import Recording
from vanilla.views import TemplateView


class GroupView(LoginRequiredMixin, TemplateView):
    template_name = 'groups/group/group_view.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self

        group_memberships = self.request.user.groupmembership_set
        groups = group_memberships.values_list('group', flat=True)

        kwargs['group_list'] = groups.order_by('-created_time')

        kwargs['recently_joined_list'] = group_memberships.order_by('-created_time') \
                                             .values_list('group', flat=True)[:6]

        # list all groups with submissions that you have permission to list
        kwargs['groups_with_submission_list'] = group_memberships.filter(authorizations__permissions=LIST_SUBMISSION) \
                                                    .annotate(submission_count=Count('submission')) \
                                                    .order_by('-submission_count')[:6]

        return kwargs

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from speakeazy.groups.models import Group

from braces.views import LoginRequiredMixin
from speakeazy.users.models import User
from vanilla.model_views import ListView


class GroupList(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups/group_list.html'

    def get_queryset(self):
        # group_memberships = GroupMembership.objects.filter(user=self.request.user)
        return Group.objects.filter(groupmembership__user=User)

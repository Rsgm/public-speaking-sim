# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from speakeazy.groups.models import Group
from braces.views import LoginRequiredMixin
from vanilla.model_views import CreateView


class NewGroup(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['name', 'description', 'parent_user_group']
    template_name = 'groups/new_group.html'

    # def get_queryset(self):
    # #group_memberships = GroupMembership.objects.filter(user=self.request.user)
    # return Group.objects.filter(group_membership__user=User)

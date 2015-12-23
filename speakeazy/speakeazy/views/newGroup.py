# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from speakeazy.speakeazy.models import Project, Group, GroupMembership
from speakeazy.users.models import User
from vanilla.model_views import ListView, CreateView


class NewGroup(LoginRequiredMixin, CreateView):
    model = Group
    # template_name = 'speakeazy/projects/group_list.html'

    # def get_queryset(self):
    # #group_memberships = GroupMembership.objects.filter(user=self.request.user)
    # return Group.objects.filter(group_membership__user=User)

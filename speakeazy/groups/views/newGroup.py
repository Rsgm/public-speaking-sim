# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.http.response import HttpResponseRedirect
from speakeazy.groups.models import Group, GroupMembership, Authorization
from braces.views import LoginRequiredMixin
from vanilla.model_views import CreateView


class NewGroup(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['name', 'description', 'parent_user_group']
    template_name = 'groups/new_group.html'

    # def get_queryset(self):
    # #group_memberships = GroupMembership.objects.filter(user=self.request.user)
    # return Group.objects.filter(group_membership__user=User)

    def form_valid(self, form):
        self.object = form.save()
        group = form.instance

        admin_authorization = Authorization(name='admin')
        admin_authorization.group = group
        admin_authorization.save()
        # admin_authorization.permissions.add() # what to use?

        membership = GroupMembership()
        membership.group = group
        membership.user = self.request.user
        membership.save()
        membership.authorizations.add(admin_authorization)

        return HttpResponseRedirect(self.get_success_url())

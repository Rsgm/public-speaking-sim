# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect, Http404

from braces.views import LoginRequiredMixin
from ratelimit.decorators import ratelimit
from speakeazy.groups.models import GroupMembership
from speakeazy.groups.views.forms import JoinForm, ERROR_MESSAGE
from vanilla.views import FormView, GenericView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class JoinGroup(LoginRequiredMixin, FormView):
    """
    Adds a user to a group using an invite form
    """
    template_name = 'groups/join_group.html'
    form_class = JoinForm

    # @ratelimit(key='user', rate='10/10s', block=True)
    def post(self, request, *args, **kwargs):
        form = self.get_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        return join(self.request, form.invite, self.request.user)


class JoinGroupLink(LoginRequiredMixin, GenericView):
    """
    Adds a user to a group using an invite link
    """
    template_name = 'groups/join_group.html'
    form_class = JoinForm

    # @ratelimit(key='user', rate='5/10s', block=True)
    def get(self, request, *args, **kwargs):
        form = JoinForm(data=kwargs)

        if not form.is_valid():
            raise Http404(ERROR_MESSAGE)

        return join(request, form.invite, self.request.user)


def join(request, invite, user):
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
        membership.roles.add(*invite.roles.all())
    else:
        # add roles to existing memberships
        membership = membership_queryset.get()
        membership.roles.add(*invite.roles.all())

    membership.save()
    messages.success(request, _('Joined group %s.' % invite.group.name))
    return HttpResponseRedirect(reverse_lazy('groups:group:groupView', kwargs={'group': membership.group.slug}))

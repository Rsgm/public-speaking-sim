# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from speakeazy.groups.mixins import GroupPermissiondMixin
from speakeazy.groups.models import Group
from speakeazy.groups.permissions import REQUEST_SUBMISSION
from speakeazy.recordings.mixins import RecordingMixin, OWNER
from speakeazy.recordings.models import SharedUser

from speakeazy.recordings.views.recording.share.forms import ShareUserForm, ShareSubmissionForm
from speakeazy.util.views import PostView
from vanilla.model_views import CreateView
from vanilla.views import TemplateView
from django.utils.translation import ugettext_lazy as _


class ListShared(RecordingMixin, TemplateView):
    pass


class CreateSharedUser(RecordingMixin, PostView):
    allowed = [OWNER]

    def get_form(self, data=None, files=None, **kwargs):
        user = self.request.user

        return ShareUserForm(initial={'user': user, 'recording': self.recording}, data=data, files=files)


class CreateSharedLink(RecordingMixin, PostView):
    pass


class CreateGroupSubmission(RecordingMixin, PostView):
    allowed = [OWNER]
    group_permission = REQUEST_SUBMISSION

    def post(self, request, *args, **kwargs):
        user = request.user
        group = get_object_or_404(Group, pk=request.POST['group'])
        permissions = set(user.groupmembership_set.filter(group=group) \
                          .values_list('authorizations__permissions__name', flat=True))

        if self.group_permission not in permissions:
            raise PermissionDenied()

        form = ShareSubmissionForm(request.user,
                                   initial={'recording': self.recording},
                                   data=request.POST,
                                   files=request.FILES)

        if not form.is_valid():
            return HttpResponse(form.errors.items)

        self.object = form.save()
        return HttpResponse(_('Group Evaluation requested.'))

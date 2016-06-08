# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from braces.views import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from speakeazy.groups.models import Group
from speakeazy.groups.permissions import REQUEST_SUBMISSION
from speakeazy.recordings.mixins import RecordingMixin, OWNER
from speakeazy.recordings.models import Recording
from speakeazy.recordings.views.settings.forms import ShareSubmissionForm, ShareUserForm

from speakeazy.util.views import PostView
from vanilla.model_views import DeleteView
from vanilla.views import TemplateView
from django.utils.translation import ugettext_lazy as _


class Delete(LoginRequiredMixin, DeleteView):
    model = Recording
    template_name = 'recordings/settings/delete.html'

    def get_object(self):
        queryset = Recording.objects.filter(pk=self.kwargs['pk'], project__user=self.request.user).select_related(
            'project')
        recording = get_object_or_404(queryset)

        self.success_url = recording.project.get_absolute_url()
        return recording


class ListShared(LoginRequiredMixin, TemplateView):
    pass


class CreateSharedUser(LoginRequiredMixin, PostView):
    allowed = [OWNER]

    def get_form(self, data=None, files=None, **kwargs):
        user = self.request.user
        recording = get_object_or_404(Recording.objects.filter(pk=kwargs['pk'], project__user=user))

        return ShareUserForm(initial={'user': user, 'recording': recording}, data=data, files=files)


class CreateSharedLink(LoginRequiredMixin, PostView):
    pass


class CreateGroupSubmission(LoginRequiredMixin, PostView):
    allowed = [OWNER]
    group_permission = REQUEST_SUBMISSION

    def post(self, request, *args, **kwargs):
        user = request.user
        group = get_object_or_404(Group, pk=request.POST['group'])
        permissions = set(user.groupmembership_set.filter(group=group)
                          .values_list('roles__permissions__name', flat=True))

        if self.group_permission not in permissions:
            raise PermissionDenied()

        recording = get_object_or_404(Recording.objects.filter(pk=kwargs['pk'], project__user=user))

        form = ShareSubmissionForm(request.user,
                                   initial={'recording': recording},
                                   data=request.POST,
                                   files=request.FILES)

        if not form.is_valid():
            return HttpResponse(form.errors.items)

        self.object = form.save()
        return HttpResponse(_('Group Evaluation requested.'))

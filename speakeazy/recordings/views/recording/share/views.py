# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.urlresolvers import reverse_lazy
from speakeazy.recordings.mixins import RecordingAuthorizationMixin, OWNER
from speakeazy.recordings.models import SharedUser

from speakeazy.recordings.views.recording.share.forms import ShareUserForm
from vanilla.model_views import CreateView
from vanilla.views import TemplateView


class CreateSubmission(RecordingAuthorizationMixin, CreateView):
    pass


class CreateSharedUser(RecordingAuthorizationMixin, CreateView):
    template_name = 'recordings/recording/share/create_shared_user.html'
    allowed = [OWNER]

    def get_form(self, data=None, files=None, **kwargs):
        user = self.request.user

        return ShareUserForm(initial={'user': user, 'recording': self.recording}, data=data, files=files)

    def get_success_url(self):
        return reverse_lazy('recordings:recording:share:list_shared', 'owner', self.object.recording.pk)


class CreateSharedLink(RecordingAuthorizationMixin, CreateView):
    pass


class ListShared(RecordingAuthorizationMixin, TemplateView):
    pass

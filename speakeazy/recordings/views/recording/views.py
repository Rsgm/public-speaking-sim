# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404
from speakeazy.recordings.mixins import RecordingAuthorizationMixin, OWNER
from speakeazy.recordings.models import EvaluationType, Recording
from speakeazy.recordings.views.recording.share.forms import ShareUserForm
from vanilla.views import TemplateView


class View(RecordingAuthorizationMixin, TemplateView):
    template_name = 'recordings/recording/recording_view.html'

    def get_context_data(self, **kwargs):
        # kwargs['view'] = self

        kwargs['recording'] = self.recording
        kwargs['authorization'] = self.authorization

        kwargs['evaluation_type_list'] = EvaluationType.objects.all()
        kwargs['evaluation_list'] = self.recording.evaluation_set.all()
        kwargs['comment_list'] = self.recording.comment_set.all()

        if self.authorization['type'] == OWNER:
            kwargs['share_user_form'] = ShareUserForm(initial={'user': self.request.user, 'recording': self.recording})

        return kwargs

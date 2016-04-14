# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from speakeazy.recordings.mixins import RecordingMixin, OWNER
from speakeazy.recordings.models import EvaluationType
from speakeazy.recordings.views.recording.share.forms import ShareUserForm, ShareSubmissionForm
from vanilla.views import TemplateView


class View(RecordingMixin, TemplateView):
    template_name = 'recordings/recording/recording_view.html'

    def get_context_data(self, **kwargs):
        user = self.request.user

        kwargs['view'] = self

        kwargs['recording'] = self.recording
        kwargs['authorization'] = self.authorization

        kwargs['evaluation_type_list'] = EvaluationType.objects.all()
        kwargs['evaluation_list'] = self.recording.evaluation_set.all()
        kwargs['comment_list'] = self.recording.comment_set.all()

        if self.authorization['type'] == OWNER:
            kwargs['share_user_form'] = ShareUserForm(initial={'recording': self.recording})
            kwargs['share_submission_form'] = ShareSubmissionForm(user, initial={'recording': self.recording})

        return kwargs

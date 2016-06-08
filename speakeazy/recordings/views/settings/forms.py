import floppyforms.__future__ as forms
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from speakeazy.groups.models import Submission, Group, GroupMembership
from speakeazy.groups.permissions import EVALUATE_SUBMISSION
from speakeazy.recordings.mixins import GRADER
from speakeazy.recordings.models import SharedUser


class ShareUserForm(forms.ModelForm):
    class Meta:
        model = SharedUser
        fields = ('comments', 'evaluations')

    def save(self, *args, **kwargs):
        self.instance.user = self.initial['user']
        self.instance.recording = self.initial['recording']
        super(ShareUserForm, self).save(*args, **kwargs)


class ShareSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('group',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.base_fields['group'].queryset = Group.objects.filter(groupmembership__user=user)

        forms.ModelForm.__init__(self, *args, **kwargs)  # not sure why this works but super().__init__() does not
        # super(ShareSubmissionForm, self).__init__(self, *args, **kwargs)

    def clean_group(self):
        group = self.cleaned_data['group']

        if self.user.group_set.filter(group=group).exists():
            raise forms.ValidationError(_('Group '))

        return group

    def save(self, *args, **kwargs):
        self.instance.recording = self.initial['recording']
        super(ShareSubmissionForm, self).save(*args, **kwargs)

        context = {
            'submission': self.instance,
            'user': self.user,
            'link_type': GRADER
        }

        plaintext = get_template('emails/group_submission.txt').render(context)
        html = get_template('emails/group_submission.html').render(context)

        msg = EmailMultiAlternatives(
            _("New Group Submission"),
            plaintext,
            settings.EMAIL_HOST_USER,
            [grader.user.email for grader in
             GroupMembership.objects.filter(group=self.instance.group, roles__permissions__name=EVALUATE_SUBMISSION)],
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

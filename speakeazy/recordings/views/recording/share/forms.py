import floppyforms.__future__ as forms
from speakeazy.groups.models import Submission, Group
from speakeazy.recordings.models import SharedUser
from django.utils.translation import ugettext_lazy as _


class ShareUserForm(forms.ModelForm):
    class Meta:
        model = SharedUser
        fields = ('comments', 'evaluations')

    def save(self, *args, **kwargs):
        self.instance.user = self.initial['user']
        self.instance.recording = self.initial['recording']
        super(ShareUserForm, self).save()


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
        super(ShareSubmissionForm, self).save()

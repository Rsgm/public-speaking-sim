import floppyforms.__future__ as forms
from speakeazy.projects.models import UserProject
from speakeazy.recordings.models import SharedUser


class ShareUserForm(forms.ModelForm):
    # user = forms.CharField()

    class Meta:
        model = SharedUser
        fields = ('comments', 'evaluations')

    # def __init__(self, recording, *args, **kwargs):
    #     self.base_fields['audience'].queryset = audiences
    #
    #     super(SharedUserForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.initial['user']
        self.instance.recording = self.initial['recording']
        super(ShareUserForm, self).save()

# class GroupSubmission(forms.ModelForm):
#     # user = forms.CharField()
#
#     class Meta:
#         model = SharedUser
#         fields = ('comments', 'evaluations')
#
#     # def __init__(self, recording, *args, **kwargs):
#     #     self.base_fields['audience'].queryset = audiences
#     #
#     #     super(SharedUserForm, self).__init__(*args, **kwargs)
#
#     def save(self, *args, **kwargs):
#         super(GroupSubmission, self).save()

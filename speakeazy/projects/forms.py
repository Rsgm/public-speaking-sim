from datetime import timedelta

import floppyforms.__future__ as forms
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext_lazy as _

from speakeazy.groups.models import Audience
from speakeazy.projects.models import UserProject, PracticeSpeech, PracticeProject
from speakeazy.util.inputs import ModelSelectField


def audience_queryset(user):
    group_list = user.group_set.values_list('id', flat=True)
    audiences = Audience.objects.filter(group__in=group_list, file_webm__isnull=False)
    return audiences


class CreateUserProjectForm(forms.ModelForm):
    class Meta:
        model = UserProject
        fields = ('name', 'description', 'audience', 'due_date')

    def __init__(self, user, *args, **kwargs):
        self.user = user  # todo: try setting initial
        self.base_fields['audience'].queryset = self.AudienceQueryset(user)

        super(CreateUserProjectForm, self).__init__()

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super(CreateUserProjectForm, self).save(*args, **kwargs)


class CreatePracticeProjectForm(forms.ModelForm):
    class Meta:
        model = PracticeProject
        fields = ('audience',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super(CreatePracticeProjectForm, self).__init__(*args, **kwargs)

        self.fields['audience'].queryset = audience_queryset(self.user)
        self.fields['speech'] = ModelSelectField(model=PracticeSpeech,
                                                 display_queryset=PracticeSpeech.objects.order_by('?')[:3],
                                                 display_values=('subject',),
                                                 required=True,
                                                 label=_("Choose a Subject That Interests You"),
                                                 label_suffix="",
                                                 help_text=_("Reload the page for new subjects"))

    def save(self, *args, **kwargs):
        speech = self.cleaned_data['speech'][0]

        self.instance.user = self.user
        self.instance.name = speech.name
        self.instance.due_date = datetime.now() + timedelta(days=7)
        self.instance.practice_speech = speech

        return super(CreatePracticeProjectForm, self).save(*args, **kwargs)

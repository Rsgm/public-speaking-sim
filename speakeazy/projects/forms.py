import floppyforms.__future__ as forms
from speakeazy.projects.models import Project


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'audience', 'due_date')

    def __init__(self, user, audiences, *args, **kwargs):
        self.user = user  # todo: try setting initial
        self.base_fields['audience'].queryset = audiences

        super(NewProjectForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super(NewProjectForm, self).save()

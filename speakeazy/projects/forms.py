import floppyforms.__future__ as forms
from speakeazy.projects.models import UserProject


class CreateUserProjectForm(forms.ModelForm):
    class Meta:
        model = UserProject
        fields = ('name', 'description', 'audience', 'due_date')

    def __init__(self, user, audiences, *args, **kwargs):
        self.user = user  # todo: try setting initial
        self.base_fields['audience'].queryset = audiences

        super(CreateUserProjectForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super(CreateUserProjectForm, self).save(*args, **kwargs)


class UserProjectForm(forms.ModelForm):
    class Meta:
        model = UserProject
        fields = ('description', 'due_date')

    def __init__(self, user, *args, **kwargs):
        self.user = user

        super(UserProjectForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super(UserProjectForm, self).save(*args, **kwargs)

import floppyforms.__future__ as forms
from speakeazy.groups.models import GroupInvite


class AddForm(forms.ModelForm):
    class Meta:
        model = GroupInvite
        fields = ('name', 'description', 'roles', 'uses', 'expires')
        widgets = {
            'expires': forms.SplitDateTimeWidget,
        }

    def __init__(self, group, *args, **kwargs):
        self.group = group
        self.base_fields['roles'].queryset = group.role_set.all()

        self.base_fields['uses'].min = 0
        self.base_fields['uses'].max = 10

        super(AddForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.group = self.group
        return super(AddForm, self).save()


class UpdateForm(forms.ModelForm):
    class Meta:
        model = GroupInvite
        fields = ('description', 'roles', 'uses', 'expires')
        widgets = {
            'expires': forms.SplitDateTimeWidget,
        }

    def __init__(self, *args, **kwargs):
        self.base_fields['roles'].queryset = self.instance.group.role_set.all()

        super(UpdateForm, self).__init__(*args, **kwargs)

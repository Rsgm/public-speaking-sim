import floppyforms.__future__ as forms
from speakeazy.groups.models import GroupInvite


class AddForm(forms.ModelForm):
    class Meta:
        model = GroupInvite
        fields = ('name', 'description', 'authorizations', 'uses', 'expires')

    def __init__(self, group, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        self.instance.group = group
        self.fields['authorizations'].queryset = group.authorization_set.all()


class UpdateForm(forms.ModelForm):
    class Meta:
        model = GroupInvite
        fields = ('description', 'authorizations', 'uses', 'expires')

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['authorizations'].queryset = self.instance.group.authorization_set.all()

import floppyforms.__future__ as forms
from speakeazy.groups.models import GroupMembership


class UpdateForm(forms.ModelForm):
    class Meta:
        model = GroupMembership
        fields = ('authorizations',)

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['authorizations'].queryset = self.instance.group.authorization_set.all()

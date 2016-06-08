import floppyforms.__future__ as forms
from speakeazy.groups.models import GroupMembership


class UpdateForm(forms.ModelForm):
    class Meta:
        model = GroupMembership
        fields = ('roles',)

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['roles'].queryset = self.instance.group.role_set.all()

import floppyforms.__future__ as forms
from speakeazy.groups.models import Audience


class AddForm(forms.ModelForm):
    class Meta:
        model = Audience
        fields = ('name', 'description')


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Audience
        fields = ('description',)

        # def __init__(self, *args, **kwargs):
        #     super(UpdateForm, self).__init__(*args, **kwargs)
        #     self.fields['authorizations'].queryset = self.instance.group.authorization_set.all()

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Submit, Layout
import floppyforms.__future__ as forms
from speakeazy.speakeazy.models import Audience, Project


class ProjectCreate(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'due_date')
        widgets = {
            'name': forms.TextInput,
            'description': forms.Textarea,
            'audience': forms.Select,
            'due_date': forms.DateInput,
        }

    def __init__(self, user, *args, **kwargs):
        super(ProjectCreate, self).__init__(*args, **kwargs)
        self.fields['audience'] = forms.ModelChoiceField(queryset=Audience.objects.filter(group__in=user.group_set.values_list('id', flat=True)))

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('name', css_class='input-xlarge'),
        Field('description', rows='2', css_class='input-xlarge'),
        Field('audience', css_class='input-xlarge'),
        Field('due_date', css_class='input-xlarge'),

        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel'),
        )
    )


    # def save(self):
    #     project = Project(**self.fields)
    #     project.save()T
    #     return project


    # def __init__(self, *args, **kwargs):
    #     u = kwargs['data']
    #     self.audience = forms.ModelChoiceField(queryset=u)
    #
    #     super(ProjectCreate, self).__init__(*args, **kwargs)

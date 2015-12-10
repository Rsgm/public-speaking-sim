from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Submit, Layout
import floppyforms.__future__ as forms
from floppyforms.widgets import TextInput
from speakeazy.speakeazy.models import Audience, Project


class ProjectCreate(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput)
    description = forms.CharField(max_length=255, widget=forms.Textarea)
    audience = forms.ModelChoiceField(queryset=None, widget=forms.Select)
    due_date = forms.DateField(widget=forms.DateInput)

    def __init__(self, audiences, *args, **kwargs):
        super(ProjectCreate, self).__init__(*args, **kwargs)
        self.fields['audience'].queryset = audiences

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
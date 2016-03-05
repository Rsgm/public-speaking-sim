from crispy_forms.layout import Layout, Field, MultiField
from django.utils.translation import ugettext
from speakeazy.projects.models import Project
from speakeazy.speakeazy_forms.ModelForm import ModelForm
from speakeazy.speakeazy_forms.layout import Row, Submit, DateField


class NewProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'audience', 'due_date')

    def __init__(self, user, audiences, *args, **kwargs):
        self.user = user
        self.base_fields['audience'].queryset = audiences

        self.helper.form_action = 'projects:newProject'
        self.helper.layout = Layout(
            MultiField(
                ugettext(''),
                Row(Field('name')),
                Row(Field('description')),
                Row(Field('audience')),
                Row(DateField('due_date')),
                Row(Submit('create', ugettext('Create'))),
            ),
        )

        super(NewProjectForm, self).__init__(*args, **kwargs)

    def save(self):
        self.instance.user = self.user
        return super(NewProjectForm, self).save()

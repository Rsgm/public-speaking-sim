import floppyforms.__future__ as forms


class ProjectCreate(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput)
    description = forms.CharField(max_length=255, widget=forms.Textarea)
    audience = forms.ModelChoiceField(queryset=None, widget=forms.Select)
    due_date = forms.DateField(widget=forms.DateInput)

    def __init__(self, audiences, *args, **kwargs):
        super(ProjectCreate, self).__init__(*args, **kwargs)
        self.fields['audience'].queryset = audiences

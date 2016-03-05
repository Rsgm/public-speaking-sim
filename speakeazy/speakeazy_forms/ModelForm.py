from crispy_forms.helper import FormHelper
from floppyforms.__future__.models import ModelForm as _ModelForm


class ModelForm(_ModelForm):
    helper = FormHelper()
    helper.form_class = 'uk-form'
    helper.html5_required = 'True'

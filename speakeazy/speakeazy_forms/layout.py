from crispy_forms.layout import Div, Field, BaseInput


class Row(Div):
    css_class = 'uk-form-row'


class DateField(Field):
    attrs = {'data-uk-datepicker': "{format:'YYYY-MM-DD'}"}


class Submit(BaseInput):
    """
    Used to create a Submit button descriptor for the {% crispy %} template tag::

        submit = Submit('Search the Site', 'search this site')

    .. note:: The first argument is also slugified and turned into the id for the submit button.
    """
    input_type = 'submit'
    field_classes = 'uk-button'

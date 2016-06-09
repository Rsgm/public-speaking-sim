import json

import floppyforms as forms
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_text
from speakeazy.util.widgets import ModelSelectWidget
from django.utils.translation import ugettext_lazy as _

CUSTOM_END_CHOICE_VALUE = -9  # -1 is taken by anonymous user, let's also skip a few just in case


class ModelSelectField(forms.ChoiceField):
    """
    A widget for selecting a single or multiple objects using the vue select component.
    """

    def __init__(self, model, display_values, multiple=False, custom_end_object=None, queryset=None, *args, **kwargs):
        """
        :param model: the type of objects to choose from, model class
        :param display_values: model attributes to display in the widget, iterable: (name, description, (list, list item name))
        :param multiple: allow multiple selections, boolean
        :param custom_end_object: an special choice to put at the end, implementation is beyond this scope, dictionary or json
        :param queryset: a queryset to filter the selection by
        :param args: passed to super
        :param kwargs: passed to super
        """

        self.model = model
        self.multiple = multiple
        self.custom_end_choice = custom_end_object is not None

        if queryset:
            self.queryset = queryset
        else:
            self.queryset = model.objects.all()

        choices = list(self.queryset.values_list('pk', flat=True))
        if custom_end_object:
            choices.append(CUSTOM_END_CHOICE_VALUE)

        widget = ModelSelectWidget(self.queryset, display_values, multiple=multiple,
                                   custom_end_object=custom_end_object)

        super(ModelSelectField, self).__init__(choices=choices, widget=widget, *args, **kwargs)

    def _set_choices(self, queryset):
        self.queryset = queryset
        choices = list(queryset.values_list('pk', flat=True))

        if self.custom_end_choice:
            choices.append(CUSTOM_END_CHOICE_VALUE)

        self._choices = self.widget.choices = choices

    def to_python(self, value):
        try:
            values = [int(v) for v in value.split(',')]
        except ValueError:
            raise ValidationError(_("Only integer lists are accepted."))

        return values

    def validate(self, value):
        """
        Validates that the input is a list or tuple.
        """
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')

        if not self.multiple and not (len(value) < 2):
            raise ValidationError(self.error_messages['requires a single value'], code='invalid_choice')

        # Validate that each value in the value list is in self.choices.
        for val in value:
            if not self.valid_value(val):
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': val},
                )

    def valid_value(self, value):
        try:
            n = int(value)
        except ValueError:
            return False

        return n in self.choices
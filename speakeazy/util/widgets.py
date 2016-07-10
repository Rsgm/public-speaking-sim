import floppyforms as forms


class ModelSelectWidget(forms.TextInput):
    template_name = 'util/widgets/select.html'

    def __init__(self, queryset, display_values, custom_end_object=None, multiple=False, *args, **kwargs):
        self.objects = []
        self.multiple = multiple
        self.custom_end_object = custom_end_object

        if len(display_values) >= 3:
            full_objects = queryset.prefetch_related(display_values[2][0])
        else:
            full_objects = queryset

        for o in full_objects:
            obj = {'id': o.pk}

            if len(display_values) >= 1:
                obj['name'] = getattr(o, display_values[0])
            if len(display_values) >= 2:
                obj['description'] = getattr(o, display_values[1])
            if len(display_values) >= 3:
                obj['list'] = getattr(o, display_values[2][0]).values_list(display_values[2][1], flat=True)

            self.objects.append(obj)

        super(ModelSelectWidget, self).__init__(*args, **kwargs)

    def get_context_data(self):
        return {
            'objects': self.objects,
            'custom_end_object': self.custom_end_object,
            'multiple': self.multiple,
            'required': self.is_required,
        }

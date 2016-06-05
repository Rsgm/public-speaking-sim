import floppyforms.__future__ as forms
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from speakeazy.groups.models import GroupInvite, GroupMembership, Group, Role, DefaultGroupStructure, DefaultGroupRole
from speakeazy.util.inputs import ModelSelectField

ERROR_MESSAGE = _('Invite does not exist or is no longer usable.')


class JoinForm(forms.Form):
    group = forms.CharField(label='Group Name', label_suffix=' (Case Sensitive):')
    token = forms.CharField(label='Token', label_suffix=' - (i.e. kfghiw)')

    invite = None

    def clean(self):
        """
        Validates the token and group

        :return: validated data
        """
        group = self.cleaned_data['group']
        token = self.cleaned_data['token']

        invite_queryset = GroupInvite.objects.filter(group__name=group, token=token)

        # make sure invite exists
        if invite_queryset.count() == 0:
            raise forms.ValidationError(ERROR_MESSAGE)

        self.invite = invite_queryset.get()

        # check expiration time
        if self.invite.expires and (timezone.now() > self.invite.expires):
            raise forms.ValidationError(ERROR_MESSAGE)

        # check uses left
        if self.invite.uses == 0:
            raise forms.ValidationError(ERROR_MESSAGE)

        return self.cleaned_data


class CreateGroupForm(forms.ModelForm):
    custom_structure_choice = {
        'id': -1,
        'name': 'Create Your Own',
        'description': 'Create a group that suits your needs.'
    }

    structure = ModelSelectField(model=DefaultGroupStructure,
                                 display_values=('name', 'description', 'default_role_types'),
                                 custom_end_object=True,
                                 required=True)

    roles = ModelSelectField(model=DefaultGroupRole,
                             display_values=('name', 'description'),
                             multiple=True,
                             required=False)

    class Meta:
        model = Group
        fields = ('name', 'description', 'logo')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateGroupForm, self).__init__(*args, **kwargs)

    def clean_structure(self):
        pk = self.cleaned_data['structure']

        if pk == -1:
            self.cleaned_data['structure'] = None
        else:
            self.cleaned_data['structure'] = get_object_or_404(DefaultGroupStructure, pk=pk)

    def save(self, *args, **kwargs):
        self.instance.save()

        membership = GroupMembership()
        membership.group = self.instance
        membership.user = self.user
        membership.save()

        default_structure = self.cleaned_data['structure']
        if default_structure:
            for default_role in default_structure.roles.all():
                role = Role()
                role.name = default_role.name
                role.group = self.instance
                role.permissions.add(default_role.permissions.all())
                role.save()

                membership.roles.add(role)  # it is best to give the user every role, instead of make an admin for them

        else:
            for i in self.cleaned_data['roles']:
                default_role = get_object_or_404(DefaultGroupRole, i)

                role = Role()
                role.name = default_role.name
                role.group = self.instance
                role.permissions.add(default_role.permissions.all())
                role.save()

                membership.roles.add(role)  # it is best to give the user every role, instead of make an admin for them

        membership.save()  # do I need to save this here?
        return super(CreateGroupForm, self).save()

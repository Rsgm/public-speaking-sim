import floppyforms.__future__ as forms
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from speakeazy.groups.models import GroupInvite, GroupMembership, Group, Role, DefaultGroupStructure, DefaultGroupRole
from speakeazy.util.inputs import ModelSelectField, CUSTOM_END_CHOICE_VALUE

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
    class Meta:
        model = Group
        fields = ('name', 'description', 'logo')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateGroupForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(CreateGroupForm, self).save(*args, **kwargs)

        membership = GroupMembership()
        membership.group = self.instance
        membership.user = self.user
        membership.save()

        return self.instance, membership


class DefaultStructureForm(forms.Form):
    custom_structure_choice = {
        'id': CUSTOM_END_CHOICE_VALUE,
        'name': 'Create Your Own',
        'description': 'Create a group that suits your needs.'
    }

    structure = ModelSelectField(model=DefaultGroupStructure,
                                 display_values=('name', 'description', ('default_role_types', 'name')),
                                 custom_end_object=custom_structure_choice,
                                 required=True)

    def clean_structure(self):
        pk = self.cleaned_data['structure'][0]

        if pk == CUSTOM_END_CHOICE_VALUE:
            return None
        else:
            try:
                return DefaultGroupStructure.objects.get(pk=pk)
            except DefaultGroupStructure.DoesNotExist:
                raise forms.ValidationError(_("Invalid group structure."))

    def save(self, group, membership):
        default_structure = self.cleaned_data['structure']

        if not default_structure:
            return None

        roles = []
        for default_role in default_structure.default_role_types.all():
            role = Role()
            role.name = default_role.name
            role.group = group
            role.save()
            role.permissions.add(*default_role.permissions.all())

            roles.append(role)

        membership.roles.add(*roles)  # it is best to give the user every role, instead of make an admin for them

        return default_structure


class DefaultRolesForm(forms.Form):
    roles = ModelSelectField(model=DefaultGroupRole,
                             display_values=('name', 'description'),
                             multiple=True,
                             required=False)

    def clean_roles(self):
        pks = self.cleaned_data['roles']
        return DefaultGroupRole.objects.filter(pk__in=pks)

    def is_valid(self, structure=None):
        self.full_clean()

        if not self.cleaned_data['roles']:
            raise forms.ValidationError(_("No group roles selected."))

        return super(DefaultRolesForm, self).is_valid()

    def save(self, group, membership):
        roles = []

        for default_role in self.cleaned_data['roles']:
            role = Role()
            role.name = default_role.name
            role.group = group
            role.save()
            role.permissions.add(*default_role.permissions.all())

            roles.append(role)

        membership.roles.add(*roles)  # it is best to give the user every role, instead of make an admin for them

        membership.save()  # do I need to save this here?

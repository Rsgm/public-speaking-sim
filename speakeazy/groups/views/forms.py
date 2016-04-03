import floppyforms.__future__ as forms
from django.utils import timezone
from speakeazy.groups.models import GroupInvite, GroupMembership, Group, Authorization
from django.utils.translation import ugettext_lazy as _

ERROR_MESSAGE = _('Invite does not exist or is no longer usable.')


class JoinForm(forms.Form):
    group = forms.CharField(help_text='help text', label='label', label_suffix=' - label suffix:')
    token = forms.CharField()

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


class NewGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'description', 'logo')

    def __init__(self, user, *args, **kwargs):
        self.user = user  # todo: try setting initial

        super(NewGroupForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.save()

        admin_authorization = Authorization(name='admin')
        admin_authorization.group = self.instance
        admin_authorization.save()
        # admin_authorization.permissions.add() # what to use?

        membership = GroupMembership()
        membership.group = self.instance
        membership.user = self.user
        membership.save()
        membership.authorizations.add(admin_authorization)

        self.instance.user = self.user
        return super(NewGroupForm, self).save()

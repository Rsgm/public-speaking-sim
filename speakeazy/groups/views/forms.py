import floppyforms.__future__ as forms
from django.utils import timezone
from speakeazy.groups.models import GroupInvite, GroupMembership, Group, Authorization


class JoinForm(forms.Form):
    group = forms.CharField()
    token = forms.CharField()

    invite = None

    def is_valid(self):
        group = self.data['group']
        token = self.data['token']

        invite_queryset = GroupInvite.objects.filter(group__name=group, token=token)

        # make sure invite exists
        if invite_queryset.count() == 0:
            return False

        self.invite = invite_queryset.get()

        # check expiration time
        if self.invite.expires and (timezone.now() > self.invite.expires):
            return False

        # check uses left
        if self.invite.uses == 0:
            return False

        return True


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
        membership.user = self.request.user
        membership.save()
        membership.authorizations.add(admin_authorization)

        self.instance.user = self.user
        return super(NewGroupForm, self).save()

import floppyforms.__future__ as forms
from django.utils import timezone
from speakeazy.groups.models import GroupInvite, GroupMembership


class JoinForm(forms.Form):
    group = forms.CharField()
    token = forms.CharField()

    def __init__(self, user=None, **kwargs):
        self.user = user
        self.membership = None
        super(JoinForm, self).__init__(**kwargs)

    def is_valid(self):
        group = self.data['group']
        token = self.data['token']

        invite_queryset = GroupInvite.objects.filter(group__name=group, token=token)

        # make sure invite exists
        if invite_queryset.count() == 0:
            return False

        invite = invite_queryset.get()

        # check expiration time
        if invite.expires and (timezone.now() > invite.expires):
            return False

        # check uses left
        if invite.uses == 0:
            return False
        elif invite.uses and invite.uses > 0:
            # subtract from uses
            invite.uses -= 1
            invite.save()

        membership_queryset = GroupMembership.objects.filter(group=invite.group, user=self.user)

        # check for existing membership
        if membership_queryset.count() == 0:
            # create membership if none exists
            self.membership = GroupMembership(group=invite.group, user=self.user)
            self.membership.save()
            self.membership.authorizations.add(*invite.authorizations.all())
        else:
            # add authorizations to existing memberships
            self.membership = membership_queryset.get()
            self.membership.authorizations.add(*invite.authorizations.all())

        self.membership.save()

        return True

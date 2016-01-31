import floppyforms.__future__ as forms
from django.utils import timezone
from speakeazy.groups.models import GroupInvite, GroupMembership


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

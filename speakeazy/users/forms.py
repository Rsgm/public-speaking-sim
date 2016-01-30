# -*- coding: utf-8 -*-
from speakeazy.groups.models import SignupMembership, GroupMembership
from userena.forms import SignupForm


class SpeakeazySignupForm(SignupForm):
    def save(self):
        new_user = super(SpeakeazySignupForm, self).save()

        signup_memberships = SignupMembership.objects.all()

        for membership in signup_memberships:
            new_membership = GroupMembership()
            new_membership.user = new_user
            new_membership.group = membership.group
            new_membership.save()

            new_membership.authorizations.add(membership.authorizations.all())

        return new_user

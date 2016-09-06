# -*- coding: utf-8 -*-
from speakeazy.groups.models import SignupMembership, GroupMembership
from userena.forms import SignupForm
from django import forms
from django.utils.translation import ugettext_lazy as _


class SpeakeazySignupForm(SignupForm):
    def clean_password1(self):
        """
        Check the password against common passwords

        :return: the validated password
        """
        print(12345678)
        with open('resources/yahoo-voices.txt', 'r') as file:
            for password in file:
                if self.cleaned_data['password1'] == password[:-1]:
                    raise forms.ValidationError(_('This password is too common.'))

        return self.cleaned_data['password1']

    def save(self):
        new_user = super(SpeakeazySignupForm, self).save()

        for membership in SignupMembership.objects.all():
            new_membership = GroupMembership()
            new_membership.user = new_user
            new_membership.group = membership.group
            new_membership.save()

            new_membership.roles.add(*membership.roles.all())

        print(12345678)
        return new_user


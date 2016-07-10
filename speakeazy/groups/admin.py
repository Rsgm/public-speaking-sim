# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from pathlib import Path

from django import forms
from django.contrib import admin
from speakeazy.groups.models import Group, GroupMembership, Role, Permission, Submission, \
    DefaultGroupRole, DefaultGroupStructure, GroupInvite, Audience, SignupMembership
from speakeazy.groups.tasks import transcode_audience
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Submission)
admin.site.register(DefaultGroupRole)
admin.site.register(DefaultGroupStructure)
admin.site.register(GroupInvite)
admin.site.register(SignupMembership)


class AudienceForm(forms.ModelForm):
    file = forms.FileField(help_text=_(""))

    class Meta:
        model = Audience
        fields = ('name', 'description', 'group')


class AudienceAdmin(admin.ModelAdmin):
    form = AudienceForm

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        self.message_user(request, "Audience processing, this may take a very long time.")

        obj.save()

        file = form.cleaned_data.get('file', None)

        audience_path = Path('%s/%s' % (settings.RECORDING_PATHS['AUDIENCE'], obj.pk)).absolute()
        with audience_path.open(mode='wb') as video:
            for chunk in file.chunks():
                video.write(chunk)

        transcode_audience.delay(obj.pk)


admin.site.register(Audience, AudienceAdmin)

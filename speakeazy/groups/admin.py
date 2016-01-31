# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from speakeazy.groups.models import Group, GroupMembership, Authorization, Permission, Submission, \
    DefaultAuthorization, DefaultGroupStructure, GroupInvite, Audience, SignupMembership

admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Authorization)
admin.site.register(Permission)
admin.site.register(Audience)
admin.site.register(Submission)
admin.site.register(DefaultAuthorization)
admin.site.register(DefaultGroupStructure)
admin.site.register(GroupInvite)
admin.site.register(SignupMembership)

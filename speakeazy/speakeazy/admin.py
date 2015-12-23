# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from speakeazy.speakeazy.models import Project, Recording, Audience, UploadPiece, Group, \
    GroupMembership, Authorization, Permission, Submission, DefaultAuthorization, DefaultGroupStructure, GroupInvite, \
    EvaluationType, Evaluation

admin.site.register(Project)
admin.site.register(Recording)
admin.site.register(Audience)
admin.site.register(UploadPiece)
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Authorization)
admin.site.register(Permission)
admin.site.register(Submission)
admin.site.register(DefaultAuthorization)
admin.site.register(DefaultGroupStructure)
admin.site.register(GroupInvite)
admin.site.register(EvaluationType)
admin.site.register(Evaluation)

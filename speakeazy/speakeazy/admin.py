# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from speakeazy.speakeazy.models import UploadPiece, Recording, Project, Audience, GroupRole, Submission, Group

admin.site.register(UploadPiece)
admin.site.register(Recording)
admin.site.register(Project)
admin.site.register(Audience)
admin.site.register(Group)
admin.site.register(GroupRole)
admin.site.register(Submission)

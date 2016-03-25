# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from userena.models import UserenaBaseProfile


@python_2_unicode_compatible
class User(AbstractUser):
    # name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('users:detail', kwargs={'username': self.username})


@python_2_unicode_compatible
class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User, unique=True, verbose_name=_('user'), related_name='my_profile')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0018_auto_20160330_0303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='state',
        ),
        migrations.AddField(
            model_name='submission',
            name='finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='grader',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]

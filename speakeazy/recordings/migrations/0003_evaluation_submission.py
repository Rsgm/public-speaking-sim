# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_remove_group_password'),
        ('recordings', '0002_auto_20160104_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='submission',
            field=models.ForeignKey(to='groups.Submission', blank=True, null=True),
        ),
    ]

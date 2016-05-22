# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0013_auto_20160131_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='group_visibility',
            field=models.ForeignKey(null=True, to='groups.Authorization', blank=True),
        ),
    ]

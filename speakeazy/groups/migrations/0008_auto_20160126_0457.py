# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0007_groupinvite_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorization',
            name='permissions',
            field=models.ManyToManyField(to='groups.Permission'),
        ),
    ]

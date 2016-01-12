# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_remove_group_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='state',
            field=models.CharField(default='r', choices=[('r', 'ready'), ('i', 'in progress'), ('f', 'finished')], max_length=1),
        ),
    ]

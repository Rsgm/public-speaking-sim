# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0017_auto_20160320_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='for_evaluation',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='group_visibility',
        ),
    ]

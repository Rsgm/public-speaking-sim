# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0004_sharedlink_shareduser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recording',
            name='slug',
        ),
    ]

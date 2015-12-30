# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20151229_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='password',
        ),
    ]

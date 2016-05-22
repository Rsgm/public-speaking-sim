# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0011_auto_20160130_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupmembership',
            name='group',
            field=models.OneToOneField(to='groups.Group'),
        ),
    ]

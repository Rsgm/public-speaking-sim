# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20160121_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorization',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Name of authorization'),
        ),
    ]

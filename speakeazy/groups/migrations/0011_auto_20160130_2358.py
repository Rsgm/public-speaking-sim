# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0010_signupmembership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupmembership',
            name='group',
            field=models.ForeignKey(to='groups.Group', unique=True),
        ),
    ]

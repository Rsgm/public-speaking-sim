# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_remove_evaluationtype_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluation',
            old_name='time',
            new_name='seconds',
        ),
    ]

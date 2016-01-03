# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20160103_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationtype',
            name='color',
        ),
    ]

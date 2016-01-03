# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20151230_2131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationtype',
            name='fa_class',
        ),
        migrations.AddField(
            model_name='evaluationtype',
            name='descritpion',
            field=models.CharField(max_length=120, default='n/a', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evaluationtype',
            name='icon_class',
            field=models.CharField(max_length=40, default='uk-icon-eye', unique=True),
            preserve_default=False,
        ),
    ]

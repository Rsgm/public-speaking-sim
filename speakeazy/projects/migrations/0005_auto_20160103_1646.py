# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20160101_2307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='seconds',
        ),
        migrations.RemoveField(
            model_name='evaluationtype',
            name='descritpion',
        ),
        migrations.AddField(
            model_name='evaluation',
            name='time',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='type',
            field=models.ForeignKey(to='projects.EvaluationType', null=True, blank=True),
        ),
    ]

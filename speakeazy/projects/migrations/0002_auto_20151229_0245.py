# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='recording',
            field=models.ForeignKey(to='recordings.Recording'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='type',
            field=models.ForeignKey(to='projects.EvaluationType'),
        ),
    ]

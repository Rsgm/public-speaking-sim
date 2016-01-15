# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20160115_0544'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recordings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='evaluator',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='recording',
            field=models.ForeignKey(to='recordings.Recording'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='submission',
            field=models.ForeignKey(null=True, to='groups.Submission', blank=True),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='type',
            field=models.ForeignKey(null=True, to='recordings.EvaluationType', blank=True),
        ),
    ]

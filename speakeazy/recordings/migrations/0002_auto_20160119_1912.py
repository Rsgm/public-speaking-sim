# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0003_auto_20160119_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='evaluator',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='recording',
            field=models.ForeignKey(to='recordings.Recording'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='submission',
            field=models.ForeignKey(null=True, blank=True, to='groups.Submission'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='type',
            field=models.ForeignKey(null=True, blank=True, to='recordings.EvaluationType'),
        ),
    ]

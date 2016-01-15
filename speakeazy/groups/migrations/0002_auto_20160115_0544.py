# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('recordings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='recording',
            field=models.ForeignKey(to='recordings.Recording'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='authorizations',
            field=models.ManyToManyField(blank=True, to='groups.Authorization', null=True),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='group',
            field=models.ForeignKey(to='groups.Group'),
        ),
    ]

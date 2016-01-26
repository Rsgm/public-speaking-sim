# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_auto_20160126_0316'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupinvite',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 1, 26, 4, 53, 16, 275223, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

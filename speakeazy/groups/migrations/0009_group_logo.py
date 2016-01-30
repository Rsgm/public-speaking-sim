# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_auto_20160126_0457'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='group-logos'),
        ),
    ]

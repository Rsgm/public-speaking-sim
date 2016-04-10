# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0020_auto_20160410_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='audience',
            name='file_mp4',
            field=models.FileField(upload_to='audience', blank=True, null=True),
        ),
    ]

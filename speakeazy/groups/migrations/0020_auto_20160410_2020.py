# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0019_auto_20160406_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audience',
            name='file',
            field=models.FileField(upload_to='audience', blank=True, null=True),
        ),
    ]

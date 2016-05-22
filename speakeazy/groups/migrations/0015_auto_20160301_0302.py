# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0014_auto_20160131_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audience',
            name='description',
            field=models.TextField(verbose_name='Description of audience', blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0003_evaluation_submission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='state',
            field=models.CharField(choices=[('u', 'uploading'), ('p', 'processing'), ('f', 'finished')], default='u', max_length=1),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_submission_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique_with=('group',), editable=False, populate_from='recording__project__name'),
        ),
    ]

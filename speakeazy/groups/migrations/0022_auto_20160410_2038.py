# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0021_audience_file_mp4'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audience',
            old_name='file',
            new_name='file_webm',
        ),
    ]

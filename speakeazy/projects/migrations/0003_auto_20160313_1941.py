# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_user'),
    ]

    operations = [
        migrations.RenameModel(old_name='Project',new_name='UserProject')
    ]

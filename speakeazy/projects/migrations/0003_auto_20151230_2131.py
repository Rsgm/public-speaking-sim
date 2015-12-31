# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20151229_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='audience',
            field=models.ForeignKey(to='groups.Audience'),
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]

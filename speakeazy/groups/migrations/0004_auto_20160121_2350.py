# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20160119_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinvite',
            name='authorizations',
            field=models.ManyToManyField(related_name='_groupinvite_authorizations_+', to='groups.Authorization', blank=True),
        ),
        migrations.AlterField(
            model_name='groupmembership',
            name='authorizations',
            field=models.ManyToManyField(to='groups.Authorization', blank=True),
        ),
    ]

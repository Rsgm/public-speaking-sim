# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20151229_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinvite',
            name='authorizations',
            field=models.ManyToManyField(related_name='_groupinvite_authorizations_+', blank=True, to='groups.Authorization', null=True),
        ),
        migrations.AlterField(
            model_name='groupmembership',
            name='authorizations',
            field=models.ManyToManyField(blank=True, to='groups.Authorization', null=True),
        ),
    ]

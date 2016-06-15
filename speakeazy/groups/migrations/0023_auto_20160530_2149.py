# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0022_auto_20160410_2038'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Authorization',
            new_name='Role',
        ),

        migrations.RenameModel(
            old_name='DefaultAuthorization',
            new_name='DefaultGroupRole',
        ),

        migrations.RenameField(
            model_name='defaultgroupstructure',
            old_name='default_authorization_types',
            new_name='default_role_types',
        ),

        migrations.RenameField(
            model_name='groupmembership',
            old_name='authorizations',
            new_name='roles',
        ),

        migrations.RenameField(
            model_name='groupinvite',
            old_name='authorizations',
            new_name='roles',
        ),

        migrations.RenameField(
            model_name='signupmembership',
            old_name='authorizations',
            new_name='roles',
        ),

        migrations.AddField(
            model_name='group',
            name='color',
            field=models.IntegerField(null=True, blank=True, verbose_name='Group color'),
        ),
    ]

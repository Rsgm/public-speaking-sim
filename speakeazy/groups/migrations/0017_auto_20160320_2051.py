# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0016_auto_20160318_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(unique=True, max_length=30, choices=[('Audience', (('list_audience', 'List audience'), ('view_audience', 'View audience'), ('add_audience', 'Add audience'), ('update_audience', 'Update audience'), ('delete_audience', 'Delete audience'))), ('User', (('list_user', 'List user'), ('view_user', 'View user'), ('update_user', 'Update user'), ('delete_user', 'Delete user'))), ('Invite', (('list_invite', 'List invite'), ('view_invite', 'View invite'), ('add_invite', 'Add invite'), ('update_invite', 'Update invite'), ('delete_invite', 'Delete invite'))), ('Submission', (('list_submission', 'List submission'), ('view_submission', 'View submission'), ('request_submission', 'Request submission'), ('update_submission', 'Update submission'), ('delete_submission', 'Delete submission'), ('evaluate_submission', 'Evaluate submission')))], verbose_name='Name of permission'),
        ),
    ]

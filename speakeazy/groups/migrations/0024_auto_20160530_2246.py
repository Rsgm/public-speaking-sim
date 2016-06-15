# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0023_auto_20160530_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultgrouprole',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description of role', null=True),
        ),
        migrations.AlterField(
            model_name='defaultgrouprole',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Name of role', unique=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='logo',
            field=models.FileField(upload_to='group-logos', blank=True, verbose_name='Group logo to display', null=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Name of role'),
        ),
    ]

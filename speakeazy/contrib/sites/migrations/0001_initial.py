# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.sites.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('domain', models.CharField(verbose_name='domain name', validators=[django.contrib.sites.models._simple_domain_name_validator], max_length=100)),
                ('name', models.CharField(verbose_name='display name', max_length=50)),
            ],
            options={
                'verbose_name': 'site',
                'db_table': 'django_site',
                'ordering': ('domain',),
                'verbose_name_plural': 'sites',
            },
            managers=[
                ('objects', django.contrib.sites.models.SiteManager()),
            ],
        ),
    ]

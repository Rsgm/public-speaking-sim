# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0009_group_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignupMembership',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('authorizations', models.ManyToManyField(blank=True, related_name='_signupmembership_authorizations_+', to='groups.Authorization')),
                ('group', models.ForeignKey(to='groups.Group')),
            ],
        ),
    ]

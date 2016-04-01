# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recordings', '0003_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('uuid', models.UUIDField(unique=True)),
                ('comments', models.BooleanField(verbose_name='Users may comment')),
                ('evaluations', models.BooleanField(verbose_name='Users may evaluate')),
                ('login_required', models.BooleanField(verbose_name='Users must be logged in')),
                ('uses', models.IntegerField(blank=True, verbose_name='Amount of times this link can be used', null=True)),
                ('expires', models.DateTimeField(blank=True, verbose_name='The date this link expires', null=True)),
                ('recording', models.ForeignKey(to='recordings.Recording')),
            ],
        ),
        migrations.CreateModel(
            name='SharedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('comments', models.BooleanField(verbose_name='Users may comment')),
                ('evaluations', models.BooleanField(verbose_name='Users may evaluate')),
                ('recording', models.ForeignKey(to='recordings.Recording')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

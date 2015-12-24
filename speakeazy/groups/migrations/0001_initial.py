# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of authorization', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultAuthorization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of authorization', unique=True)),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description of authorization')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultGroupStructure',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of group structure', unique=True)),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description of group structure')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of group')),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description of group')),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique=True)),
                ('password', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupInvite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('token', models.CharField(max_length=20, unique=True)),
                ('uses', models.IntegerField()),
                ('expires', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of permission', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('for_evaluation', models.BooleanField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='recording.project.name', editable=False, unique_with=('group',))),
                ('group', models.ForeignKey(to='groups.Group')),
                ('group_visibility', models.ForeignKey(to='groups.Authorization')),
            ],
        ),
    ]

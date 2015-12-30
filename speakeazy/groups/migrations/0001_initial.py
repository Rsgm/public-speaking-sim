# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name of audience', max_length=60)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description of project')),
                ('file', models.FileField(upload_to='audience')),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique_with=('group',))),
            ],
        ),
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, verbose_name='Name of authorization', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultAuthorization',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, verbose_name='Name of authorization', max_length=30)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description of authorization')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultGroupStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, verbose_name='Name of group structure', max_length=30)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description of group structure')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name of group', max_length=30)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description of group')),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique=True)),
                ('password', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name of invite', max_length=30)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description of invite')),
                ('token', models.CharField(max_length=16)),
                ('uses', models.IntegerField(blank=True, null=True)),
                ('expires', models.DateTimeField(blank=True, null=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique_with=('group',))),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, verbose_name='Name of permission', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('for_evaluation', models.BooleanField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='recording.project.name', editable=False, unique_with=('group',))),
                ('group', models.ForeignKey(to='groups.Group')),
                ('group_visibility', models.ForeignKey(to='groups.Authorization')),
            ],
        ),
    ]

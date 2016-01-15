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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name of audience', max_length=60)),
                ('description', models.TextField(verbose_name='Description of project', blank=True, null=True)),
                ('file', models.FileField(upload_to='audience')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique_with=('group',), populate_from='name')),
            ],
        ),
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name='Name of authorization')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultAuthorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name='Name of authorization')),
                ('description', models.TextField(verbose_name='Description of authorization', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultGroupStructure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name='Name of group structure')),
                ('description', models.TextField(verbose_name='Description of group structure', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name of group', max_length=30)),
                ('description', models.TextField(verbose_name='Description of group', blank=True, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, populate_from='name', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='GroupInvite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name of invite', max_length=30)),
                ('description', models.TextField(verbose_name='Description of invite', blank=True, null=True)),
                ('token', models.CharField(max_length=16)),
                ('uses', models.IntegerField(blank=True, null=True)),
                ('expires', models.DateTimeField(blank=True, null=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique_with=('group',), populate_from='name')),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name='Name of permission')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('for_evaluation', models.BooleanField()),
                ('state', models.CharField(choices=[('r', 'ready'), ('i', 'in progress'), ('f', 'finished')], max_length=1, default='r')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(to='groups.Group')),
                ('group_visibility', models.ForeignKey(to='groups.Authorization')),
            ],
        ),
    ]

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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Name of audience')),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description of project')),
                ('file', models.FileField(upload_to='audience')),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', unique_with=('group',), editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name of authorization', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultAuthorization',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name of authorization', unique=True)),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description of authorization')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultGroupStructure',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name of group structure', unique=True)),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description of group structure')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name of group')),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description of group')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', unique=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='GroupInvite',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name of invite')),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description of invite')),
                ('token', models.CharField(max_length=16)),
                ('uses', models.IntegerField(null=True, blank=True)),
                ('expires', models.DateTimeField(null=True, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', unique_with=('group',), editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name of permission', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('for_evaluation', models.BooleanField()),
                ('state', models.CharField(max_length=1, choices=[('r', 'ready'), ('i', 'in progress'), ('f', 'finished')], default='r')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(to='groups.Group')),
                ('group_visibility', models.ForeignKey(to='groups.Authorization')),
            ],
        ),
    ]

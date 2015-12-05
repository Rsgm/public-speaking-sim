# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=60, verbose_name='Name of audience')),
                ('description', models.CharField(max_length=255, blank=True, verbose_name='Description of project')),
                ('user_created', models.BooleanField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of authorization', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultAuthorization',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of authorization', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultGroupStructure',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of authorization', unique=True)),
                ('default_authorization_types', models.ManyToManyField(to='speakeazy.DefaultAuthorization')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of group')),
                ('description', models.CharField(max_length=255, blank=True, verbose_name='Description of group')),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique=True)),
                ('parent_user_group', models.ForeignKey(to='speakeazy.Group', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('authorization', models.ManyToManyField(to='speakeazy.Authorization')),
                ('group', models.ForeignKey(to='speakeazy.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of permission', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of project')),
                ('description', models.CharField(max_length=255, blank=True, verbose_name='Description of project')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique_with=('user',))),
                ('audience', models.ForeignKey(to='speakeazy.Audience', editable=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('state', models.CharField(max_length=1, default='u', choices=[('u', 'uploading'), ('p', 'processing'), ('r', 'finished')])),
                ('finish_time', models.DateTimeField()),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('slug', autoslug.fields.AutoSlugField(unique_with=('project',))),
                ('project', models.ForeignKey(to='speakeazy.Project', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('for_evaluation', models.BooleanField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='recording.project.name', editable=False, unique_with=('group',))),
                ('group', models.ForeignKey(to='speakeazy.Group')),
                ('group_visibility', models.ForeignKey(to='speakeazy.Authorization')),
                ('recording', models.ForeignKey(to='speakeazy.Recording')),
            ],
        ),
        migrations.CreateModel(
            name='UploadPiece',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('recording', models.ForeignKey(to='speakeazy.Recording')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='speakeazy.GroupMembership'),
        ),
        migrations.AddField(
            model_name='defaultauthorization',
            name='permissions',
            field=models.ManyToManyField(to='speakeazy.Permission', related_name='_defaultauthorization_permissions_+'),
        ),
        migrations.AddField(
            model_name='authorization',
            name='group',
            field=models.ForeignKey(to='speakeazy.Group'),
        ),
        migrations.AddField(
            model_name='authorization',
            name='permissions',
            field=models.ManyToManyField(to='speakeazy.Permission'),
        ),
        migrations.AddField(
            model_name='audience',
            name='group',
            field=models.ForeignKey(to='speakeazy.Group'),
        ),
    ]

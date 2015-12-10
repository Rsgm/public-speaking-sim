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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Name of audience')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Description of project')),
                ('user_created', models.BooleanField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Name of authorization')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultAuthorization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Name of authorization')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultGroupStructure',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Name of authorization')),
                ('default_authorization_types', models.ManyToManyField(to='speakeazy.DefaultAuthorization')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name of group')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Description of group')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('parent_user_group', models.ForeignKey(to='speakeazy.Group', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('authorization', models.ManyToManyField(to='speakeazy.Authorization')),
                ('group', models.ForeignKey(to='speakeazy.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Name of permission')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name of project')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Description of project')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique_with=('user',), populate_from='name')),
                ('audience', models.ForeignKey(editable=False, to='speakeazy.Audience')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('state', models.CharField(max_length=1, default='u', choices=[('u', 'uploading'), ('p', 'processing'), ('r', 'finished')])),
                ('finish_time', models.DateTimeField(null=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('slug', autoslug.fields.AutoSlugField(unique_with=('project',))),
                ('project', models.ForeignKey(editable=False, to='speakeazy.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('for_evaluation', models.BooleanField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique_with=('group',), populate_from='recording.project.name')),
                ('group', models.ForeignKey(to='speakeazy.Group')),
                ('group_visibility', models.ForeignKey(to='speakeazy.Authorization')),
                ('recording', models.ForeignKey(to='speakeazy.Recording')),
            ],
        ),
        migrations.CreateModel(
            name='UploadPiece',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('recording', models.ForeignKey(to='speakeazy.Recording')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(through='speakeazy.GroupMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='defaultauthorization',
            name='permissions',
            field=models.ManyToManyField(related_name='_defaultauthorization_permissions_+', to='speakeazy.Permission'),
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

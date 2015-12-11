# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Name of audience', max_length=60)),
                ('description', models.CharField(verbose_name='Description of project', blank=True, max_length=255)),
                ('file', models.FileField(upload_to='audience')),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', unique=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, verbose_name='Name of authorization', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultAuthorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, verbose_name='Name of authorization', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultGroupStructure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, verbose_name='Name of authorization', max_length=30)),
                ('default_authorization_types', models.ManyToManyField(to='speakeazy.DefaultAuthorization')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Name of group', max_length=30)),
                ('description', models.CharField(verbose_name='Description of group', blank=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', unique=True, editable=False)),
                ('parent_user_group', models.ForeignKey(null=True, blank=True, to='speakeazy.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('authorization', models.ManyToManyField(to='speakeazy.Authorization')),
                ('group', models.ForeignKey(to='speakeazy.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, verbose_name='Name of permission', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Name of project', max_length=30)),
                ('description', models.CharField(verbose_name='Description of project', blank=True, max_length=255)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', unique_with=('user',), editable=False)),
                ('audience', models.ForeignKey(editable=False, to='speakeazy.Audience')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('state', models.CharField(choices=[('u', 'uploading'), ('p', 'processing'), ('r', 'finished')], max_length=1, default='u')),
                ('finish_time', models.DateTimeField(null=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('video', models.FileField(upload_to='recordings')),
                ('thumbnail_image', models.FileField(upload_to='thumbnails')),
                ('thumbnail_video', models.FileField(upload_to='thumbnails')),
                ('slug', autoslug.fields.AutoSlugField(unique_with=('project',))),
                ('project', models.ForeignKey(editable=False, to='speakeazy.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('for_evaluation', models.BooleanField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='recording.project.name', unique_with=('group',), editable=False)),
                ('group', models.ForeignKey(to='speakeazy.Group')),
                ('group_visibility', models.ForeignKey(to='speakeazy.Authorization')),
                ('recording', models.ForeignKey(to='speakeazy.Recording')),
            ],
        ),
        migrations.CreateModel(
            name='UploadPiece',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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

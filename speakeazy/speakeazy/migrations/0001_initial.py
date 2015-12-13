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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name of audience', max_length=60)),
                ('description', models.CharField(verbose_name='Description of project', max_length=255, blank=True)),
                ('file', models.FileField(upload_to='audience')),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name of authorization', unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultAuthorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name of authorization', unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultGroupStructure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name of authorization', unique=True, max_length=30)),
                ('default_authorization_types', models.ManyToManyField(to='speakeazy.DefaultAuthorization')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name of group', max_length=30)),
                ('description', models.CharField(verbose_name='Description of group', max_length=255, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique=True)),
                ('parent_user_group', models.ForeignKey(to='speakeazy.Group', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authorization', models.ManyToManyField(to='speakeazy.Authorization')),
                ('group', models.ForeignKey(to='speakeazy.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name of permission', unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name of project', max_length=30)),
                ('description', models.CharField(verbose_name='Description of project', max_length=255, blank=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(unique_with=('user',), populate_from='name', editable=False)),
                ('audience', models.ForeignKey(to='speakeazy.Audience', editable=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(choices=[('u', 'uploading'), ('p', 'processing'), ('r', 'finished')], max_length=1, default='u')),
                ('finish_time', models.DateTimeField(null=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('video', models.FileField(upload_to='recordings')),
                ('thumbnail_image', models.FileField(upload_to='thumbnails')),
                ('thumbnail_video', models.FileField(upload_to='thumbnails')),
                ('slug', models.IntegerField()),
                ('project', models.ForeignKey(to='speakeazy.Project', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('for_evaluation', models.BooleanField()),
                ('slug', autoslug.fields.AutoSlugField(unique_with=('group',), populate_from='recording.project.name', editable=False)),
                ('group', models.ForeignKey(to='speakeazy.Group')),
                ('group_visibility', models.ForeignKey(to='speakeazy.Authorization')),
                ('recording', models.ForeignKey(to='speakeazy.Recording')),
            ],
        ),
        migrations.CreateModel(
            name='UploadPiece',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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

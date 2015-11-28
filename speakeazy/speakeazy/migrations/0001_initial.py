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
                ('user_created', models.BooleanField()),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='name')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Name of group', max_length=30)),
                ('description', models.CharField(verbose_name='Description of group', blank=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from='name')),
                ('parent_group', models.ForeignKey(null=True, to='speakeazy.Group', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('role', models.CharField(default='u', choices=[('a', 'admin'), ('g', 'grader'), ('u', 'speakeazy')], max_length=1)),
                ('group', models.ForeignKey(to='speakeazy.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique_with=('user',))),
                ('audience', models.ForeignKey(to='speakeazy.Audience', editable=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('state', models.CharField(default='n', choices=[('n', 'not started'), ('p', 'processing'), ('r', 'finished')], max_length=1)),
                ('finish_time', models.DateTimeField()),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(to='speakeazy.Project', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('for_evaluation', models.BooleanField()),
                ('role_visibility', models.CharField(choices=[('a', 'admin'), ('g', 'grader'), ('u', 'speakeazy')], max_length=1)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='recording.project.name', unique_with=('group',))),
                ('group', models.ForeignKey(to='speakeazy.Group')),
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
            model_name='audience',
            name='group',
            field=models.ForeignKey(to='speakeazy.Group'),
        ),
    ]

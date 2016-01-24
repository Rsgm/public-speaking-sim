# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('text', models.TextField()),
                ('seconds', models.IntegerField(null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('icon_class', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('state', models.CharField(max_length=1, choices=[('u', 'uploading'), ('p', 'processing'), ('f', 'finished')], default='u')),
                ('finish_time', models.DateTimeField(null=True, blank=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('duration', models.IntegerField(null=True, blank=True)),
                ('video', models.FileField(null=True, blank=True, upload_to='recordings')),
                ('thumbnail_image', models.FileField(null=True, blank=True, upload_to='thumbnails')),
                ('thumbnail_video', models.FileField(null=True, blank=True, upload_to='thumbnails')),
                ('slug', models.IntegerField()),
                ('project', models.ForeignKey(to='projects.Project', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='UploadPiece',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('recording', models.ForeignKey(to='recordings.Recording')),
            ],
        ),
    ]

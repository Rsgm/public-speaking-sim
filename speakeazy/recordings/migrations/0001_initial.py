# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('state', models.CharField(max_length=1, default='u', choices=[('u', 'uploading'), ('p', 'processing'), ('r', 'finished')])),
                ('finish_time', models.DateTimeField(null=True, blank=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('duration', models.IntegerField(null=True, blank=True)),
                ('video', models.FileField(null=True, blank=True, upload_to='recordings')),
                ('thumbnail_image', models.FileField(null=True, blank=True, upload_to='thumbnails')),
                ('thumbnail_video', models.FileField(null=True, blank=True, upload_to='thumbnails')),
                ('slug', models.IntegerField()),
                ('project', models.ForeignKey(editable=False, to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='UploadPiece',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('recording', models.ForeignKey(to='recordings.Recording')),
            ],
        ),
    ]

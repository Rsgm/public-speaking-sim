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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('state', models.CharField(choices=[('u', 'uploading'), ('p', 'processing'), ('r', 'finished')], default='u', max_length=1)),
                ('finish_time', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('video', models.FileField(blank=True, upload_to='recordings', null=True)),
                ('thumbnail_image', models.FileField(blank=True, upload_to='thumbnails', null=True)),
                ('thumbnail_video', models.FileField(blank=True, upload_to='thumbnails', null=True)),
                ('slug', models.IntegerField()),
                ('project', models.ForeignKey(editable=False, to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='UploadPiece',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('recording', models.ForeignKey(to='recordings.Recording')),
            ],
        ),
    ]

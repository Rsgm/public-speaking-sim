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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.TextField()),
                ('seconds', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('icon_class', models.CharField(unique=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('state', models.CharField(choices=[('u', 'uploading'), ('p', 'processing'), ('f', 'finished')], max_length=1, default='u')),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('recording', models.ForeignKey(to='recordings.Recording')),
            ],
        ),
    ]

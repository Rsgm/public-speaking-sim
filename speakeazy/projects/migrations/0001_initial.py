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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=60, verbose_name='Name of audience')),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description of project')),
                ('file', models.FileField(upload_to='audience')),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('text', models.TextField()),
                ('seconds', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('evaluator', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('color', models.CharField(max_length=6, unique=True)),
                ('fa_class', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name of project')),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description of project')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique_with=('user',))),
                ('audience', models.ForeignKey(editable=False, to='projects.Audience')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

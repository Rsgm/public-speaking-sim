# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('seconds', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('evaluator', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('color', models.CharField(unique=True, max_length=6)),
                ('fa_class', models.CharField(unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name of project', max_length=30)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description of project')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False, unique_with=('user',))),
                ('audience', models.ForeignKey(editable=False, to='groups.Audience')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

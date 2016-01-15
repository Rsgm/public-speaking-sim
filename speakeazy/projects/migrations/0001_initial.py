# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name of project', max_length=30)),
                ('description', models.TextField(verbose_name='Description of project', blank=True, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique_with=('user',), populate_from='name')),
                ('audience', models.ForeignKey(to='groups.Audience')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, unique_with=('user',), populate_from='name')),
                ('audience', models.ForeignKey(to='groups.Audience')),
                ('project', models.OneToOneField(to='projects.Project')),
            ],
        ),
    ]

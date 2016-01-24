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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name of project')),
                ('description', models.TextField(null=True, blank=True, verbose_name='Description of project')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', unique_with=('user',), editable=False)),
                ('audience', models.ForeignKey(to='groups.Audience')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', unique_with=('user',), editable=False)),
                ('audience', models.ForeignKey(to='groups.Audience')),
                ('project', models.OneToOneField(to='projects.Project')),
            ],
        ),
    ]

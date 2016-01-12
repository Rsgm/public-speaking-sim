# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_remove_group_password'),
        ('projects', '0007_auto_20160104_0538'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateField()),
                ('slug', autoslug.fields.AutoSlugField(unique_with=('user',), editable=False, populate_from='name')),
                ('audience', models.ForeignKey(to='groups.Audience')),
                ('project', models.OneToOneField(to='projects.Project')),
            ],
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='evaluator',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='recording',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='type',
        ),
        migrations.DeleteModel(
            name='Evaluation',
        ),
        migrations.DeleteModel(
            name='EvaluationType',
        ),
    ]

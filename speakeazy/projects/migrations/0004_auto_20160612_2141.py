# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20160313_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='PracticeProject',
            fields=[
                ('userproject_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, primary_key=True, to='projects.UserProject')),
            ],
            options={
                'abstract': False,
            },
            bases=('projects.userproject',),
        ),
        migrations.CreateModel(
            name='PracticeSpeech',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Name of Speech')),
                ('subject', models.CharField(max_length=30, verbose_name='A General Subject This Speech Covers')),
                ('time_length', models.IntegerField(verbose_name='Estimated Recording Duration')),
                ('text', models.TextField(verbose_name='Speech Text')),
            ],
        ),
        migrations.AlterField(
            model_name='userproject',
            name='name',
            field=models.CharField(max_length=60, verbose_name='Name of project'),
        ),
        migrations.AddField(
            model_name='practiceproject',
            name='practice_speech',
            field=models.ForeignKey(to='projects.PracticeSpeech'),
        ),
    ]

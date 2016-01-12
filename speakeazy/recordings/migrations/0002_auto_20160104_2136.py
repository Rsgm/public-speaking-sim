# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recordings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('seconds', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('evaluator', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('recording', models.ForeignKey(to='recordings.Recording')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('icon_class', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='evaluation',
            name='type',
            field=models.ForeignKey(blank=True, null=True, to='recordings.EvaluationType'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import easy_thumbnails.fields
import userena.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, blank=True, verbose_name='mugshot')),
                ('privacy', models.CharField(help_text='Designates who can view your profile.', choices=[('open', 'Open'), ('registered', 'Registered'), ('closed', 'Closed')], max_length=15, verbose_name='privacy', default='closed')),
                ('user', models.OneToOneField(related_name='my_profile', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
        ),
    ]

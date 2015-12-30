# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('recordings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='recording',
            field=models.ForeignKey(to='recordings.Recording'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='authorizations',
            field=models.ManyToManyField(to='groups.Authorization'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='group',
            field=models.ForeignKey(to='groups.Group'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupinvite',
            name='authorizations',
            field=models.ManyToManyField(to='groups.Authorization', related_name='_groupinvite_authorizations_+'),
        ),
        migrations.AddField(
            model_name='groupinvite',
            name='group',
            field=models.ForeignKey(to='groups.Group'),
        ),
        migrations.AddField(
            model_name='group',
            name='parent_user_group',
            field=models.ForeignKey(blank=True, null=True, to='groups.Group'),
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(through='groups.GroupMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='defaultgroupstructure',
            name='default_authorization_types',
            field=models.ManyToManyField(to='groups.DefaultAuthorization'),
        ),
        migrations.AddField(
            model_name='defaultauthorization',
            name='permissions',
            field=models.ManyToManyField(to='groups.Permission', related_name='_defaultauthorization_permissions_+'),
        ),
        migrations.AddField(
            model_name='authorization',
            name='group',
            field=models.ForeignKey(to='groups.Group'),
        ),
        migrations.AddField(
            model_name='authorization',
            name='permissions',
            field=models.ManyToManyField(to='groups.Permission'),
        ),
        migrations.AddField(
            model_name='audience',
            name='group',
            field=models.ForeignKey(to='groups.Group'),
        ),
    ]

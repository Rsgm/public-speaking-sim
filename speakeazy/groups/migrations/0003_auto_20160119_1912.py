# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0002_auto_20160119_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmembership',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupinvite',
            name='authorizations',
            field=models.ManyToManyField(related_name='_groupinvite_authorizations_+', null=True, blank=True, to='groups.Authorization'),
        ),
        migrations.AddField(
            model_name='groupinvite',
            name='group',
            field=models.ForeignKey(to='groups.Group'),
        ),
        migrations.AddField(
            model_name='group',
            name='parent_user_group',
            field=models.ForeignKey(null=True, blank=True, to='groups.Group'),
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
            field=models.ManyToManyField(related_name='_defaultauthorization_permissions_+', to='groups.Permission'),
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

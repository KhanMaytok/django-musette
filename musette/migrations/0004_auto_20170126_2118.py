# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-27 00:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musette', '0003_auto_20170124_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='like',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='topic',
            name='like',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-06 03:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musette', '0005_likecomment_liketopic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='is_close',
            field=models.BooleanField(default=False, help_text='If the topic is closed', verbose_name='Closed topic'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 12:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='author',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tags',
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.CharField(default=datetime.datetime(2016, 4, 22, 12, 17, 31, 826711, tzinfo=utc), max_length=20),
            preserve_default=False,
        ),
    ]

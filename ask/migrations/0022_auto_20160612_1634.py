# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-12 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0021_remove_question_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='ask.Tag'),
        ),
    ]

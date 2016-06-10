# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-23 17:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0005_profile_question_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(blank=True)),
                ('rating', models.IntegerField()),
                ('is_correct', models.BooleanField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.Profile')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'ask_answers',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.Profile'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='question',
            name='tags',
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='ask.Tag'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.Question'),
        ),
    ]

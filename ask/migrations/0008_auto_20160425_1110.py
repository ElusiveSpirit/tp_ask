# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 11:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0007_auto_20160423_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='answer',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='question',
            name='rating',
        ),
        migrations.AlterField(
            model_name='answer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='like',
            name='answer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='ask.Answer'),
        ),
        migrations.AddField(
            model_name='like',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.Profile'),
        ),
        migrations.AddField(
            model_name='like',
            name='question',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='ask.Question'),
        ),
    ]

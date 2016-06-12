# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-09 18:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ask', '0012_auto_20160429_1003'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='profile',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='profile',
            name='id',
            field=models.AutoField(auto_created=True, default=-1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
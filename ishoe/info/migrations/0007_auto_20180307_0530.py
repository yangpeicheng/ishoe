# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-07 05:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_auto_20180307_0523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensortag',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

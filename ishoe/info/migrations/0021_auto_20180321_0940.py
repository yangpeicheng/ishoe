# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-21 09:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0020_auto_20180321_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-21 08:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0019_rpi_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='heartbeat',
            name='rpi',
        ),
        migrations.DeleteModel(
            name='Heartbeat',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-06 03:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('birth', models.DateField()),
                ('ble_mac', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Rpi',
            fields=[
                ('ip', models.CharField(default='192.1.2.105', max_length=30, primary_key=True, serialize=False)),
                ('location', models.CharField(default='001', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sensortag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('light', models.FloatField()),
                ('acc_x', models.FloatField()),
                ('acc_y', models.FloatField()),
                ('acc_z', models.FloatField()),
                ('gyro_x', models.FloatField()),
                ('gyro_y', models.FloatField()),
                ('gyro_z', models.FloatField()),
                ('magn_x', models.FloatField()),
                ('magn_y', models.FloatField()),
                ('magn_z', models.FloatField()),
                ('move_flag', models.BooleanField(default=False)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Person')),
                ('rpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Rpi')),
            ],
        ),
    ]

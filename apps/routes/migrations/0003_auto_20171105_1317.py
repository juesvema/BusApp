# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-05 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0002_auto_20171105_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrivaltime',
            name='time',
            field=models.TimeField(blank=True, null=True, verbose_name='Hora de llegada'),
        ),
    ]

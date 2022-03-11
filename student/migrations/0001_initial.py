# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-02 15:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Queries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentID', models.CharField(max_length=100)),
                ('courseID', models.CharField(max_length=100)),
                ('query', models.CharField(max_length=1000)),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('resolved', models.BooleanField(default=False)),
            ],
        ),
    ]
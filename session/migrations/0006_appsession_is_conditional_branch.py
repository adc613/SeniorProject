# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0005_auto_20160414_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='appsession',
            name='is_conditional_branch',
            field=models.BooleanField(default=False),
        ),
    ]
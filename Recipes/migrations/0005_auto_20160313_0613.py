# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-13 06:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Recipes', '0004_auto_20160310_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalaction',
            name='instruction_number',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='generalaction',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='Recipes.Recipe'),
        ),
    ]

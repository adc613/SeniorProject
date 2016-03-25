# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APICall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=2048)),
                ('is_get', models.BooleanField(default=True)),
                ('json_string', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BasicReturnText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_statement', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ConditionalHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instruction_number', models.IntegerField(default=-1)),
                ('type', models.CharField(choices=[('NS', 'Not Specified'), ('RT', 'Basic Return Text'), ('C', 'Conditional')], default='RT', max_length=2)),
                ('is_api_call', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_conditional_branch', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('branch_number', models.IntegerField(default=-1)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-07 05:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from accounts.models import User


class Migration(migrations.Migration):
    user = User.objects.get(pk=1)

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('program_counter', models.IntegerField()),
                ('end', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameField(
            model_name='generalaction',
            old_name='ReturnStatement',
            new_name='return_statement',
        ),
        migrations.RemoveField(
            model_name='generalaction',
            name='NextAction',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='FirstAction',
        ),
        migrations.AddField(
            model_name='generalaction',
            name='instruction_number',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generalaction',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='Recipes.Recipe'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generalaction',
            name='type',
            field=models.CharField(choices=[('RT', 'Basic Return Text')], default='RT', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appsession',
            name='current_app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Recipes.Recipe'),
        ),
        migrations.AddField(
            model_name='appsession',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

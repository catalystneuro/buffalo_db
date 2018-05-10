# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-10 21:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0004_lab'),
        ('actions', '0006_auto_20180319_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='otheraction',
            name='lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.Lab'),
        ),
        migrations.AddField(
            model_name='session',
            name='lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.Lab'),
        ),
        migrations.AddField(
            model_name='surgery',
            name='lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.Lab'),
        ),
        migrations.AddField(
            model_name='virusinjection',
            name='lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.Lab'),
        ),
        migrations.AddField(
            model_name='waterrestriction',
            name='lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.Lab'),
        ),
    ]

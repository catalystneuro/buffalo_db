# Generated by Django 3.0.6 on 2020-06-10 20:34

import buffalo.models
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('buffalo', '0002_auto_20200610_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stlfile',
            name='stl_file',
            field=models.FileField(upload_to=buffalo.models.stl_directory_path, validators=[django.core.validators.FileExtensionValidator(['stl'])]),
        ),
        migrations.CreateModel(
            name='StartingPointSet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='buffalo.BuffaloSubject')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='startingpoint',
            name='starting_point_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='starting_point', to='buffalo.StartingPointSet'),
        ),
    ]

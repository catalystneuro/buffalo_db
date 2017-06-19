# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-29 10:36
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0005_auto_20170529_1136'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0001_initial'),
    ]

    operations = [

        migrations.DeleteModel(
            name='ArchiveDataRepository',
        ),
        migrations.DeleteModel(
            name='LocalDataRepository',
        ),
        migrations.DeleteModel(
            name='NetworkDataRepository',
        ),
        migrations.DeleteModel(
            name='PhysicalArchive',
        ),


        migrations.CreateModel(
            name='DataRepositoryType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DatasetType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('name', models.CharField(blank=True, help_text='description of data type', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventSeries',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='The creation date.', null=True)),
                ('description', models.TextField(blank=True, help_text="misc. narrative e.g. 'drifting gratings of different orientations', 'ChoiceWorld behavior events'")),
                ('generating_software', models.CharField(blank=True, help_text="e.g. 'ChoiceWorld 0.8.3'", max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Event series',
            },
        ),
        migrations.CreateModel(
            name='IntervalSeries',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='The creation date.', null=True)),
                ('description', models.TextField(blank=True, help_text="misc. narrative e.g. 'drifting gratings of different orientations', 'ChoiceWorld behavior intervals'")),
                ('generating_software', models.CharField(blank=True, help_text="e.g. 'ChoiceWorld 0.8.3'", max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Interval series',
            },
        ),
        migrations.CreateModel(
            name='Timescale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='The creation date.', null=True)),
                ('name', models.CharField(blank=True, help_text='informal name describing this field', max_length=255)),
                ('nominal_start', models.DateTimeField(blank=True, help_text='Approximate date and time corresponding to 0 samples', null=True)),
                ('nominal_time_unit', models.FloatField(blank=True, help_text='Nominal time unit for this timescale (in seconds)', null=True)),
                ('final', models.BooleanField(help_text='set to true for the final results of time alignment, in seconds')),
                ('info', models.CharField(blank=True, help_text='any information, e.g. length of break around 300s inferred approximately from computer clock', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Time scales',
            },
        ),
        migrations.RemoveField(
            model_name='timestamp',
            name='dataset_ptr',
        ),
        migrations.RemoveField(
            model_name='datarepository',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='filerecord',
            name='filename',
        ),
        migrations.RemoveField(
            model_name='timeseries',
            name='column_names',
        ),
        migrations.RemoveField(
            model_name='timeseries',
            name='description',
        ),
        migrations.RemoveField(
            model_name='timeseries',
            name='file',
        ),
        migrations.AddField(
            model_name='datarepository',
            name='path',
            field=models.CharField(blank=True, help_text='absolute path to the repository', max_length=1000),
        ),
        migrations.AddField(
            model_name='dataset',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='The creator of the data.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_dataset_created_by_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dataset',
            name='created_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='The creation date.', null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='md5',
            field=models.UUIDField(blank=True, help_text='MD5 hash of the data buffer', null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='session',
            field=models.ForeignKey(blank=True, help_text='The Session to which this data belongs', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_dataset_session_related', to='actions.Session'),
        ),
        migrations.AddField(
            model_name='filerecord',
            name='data_repository',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.DataRepository'),
        ),
        migrations.AddField(
            model_name='filerecord',
            name='relative_path',
            field=models.CharField(blank=True, help_text='path name within repository', max_length=1000),
        ),
        migrations.AddField(
            model_name='timeseries',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='The creator of the data.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_timeseries_created_by_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='timeseries',
            name='created_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='The creation date.', null=True),
        ),
        migrations.AddField(
            model_name='timeseries',
            name='data',
            field=models.ForeignKey(blank=True, help_text='N*2 array containing sample numbers and their associated timestamps', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_timeseries_data_related', to='data.Dataset'),
        ),
        migrations.AlterField(
            model_name='filerecord',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_filerecord_dataset_related', to='data.Dataset'),
        ),
        migrations.AlterField(
            model_name='timeseries',
            name='session',
            field=models.ForeignKey(blank=True, help_text='The Session to which this data belongs', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_timeseries_session_related', to='actions.Session'),
        ),
        migrations.RemoveField(
            model_name='timeseries',
            name='timestamps',
        ),
        migrations.AddField(
            model_name='timeseries',
            name='timestamps',
            field=models.ForeignKey(blank=True, help_text='N*2 array containing sample numbers and their associated timestamps', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_timeseries_timestamps_related', to='data.Dataset'),
        ),
    ]

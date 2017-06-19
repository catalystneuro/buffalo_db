# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 11:46
from __future__ import unicode_literals

import datetime
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appliance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('serial', models.CharField(blank=True, help_text='The serial number of the appliance.', max_length=255)),
                ('notes', models.TextField(blank=True)),
                ('descriptive_name', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EquipmentModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('model_name', models.CharField(help_text="e.g. 'BrainScanner 4X'", max_length=255)),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LabLocation',
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
            name='Supplier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('name', models.CharField(help_text="i.e. 'NeuroNexus'", max_length=255)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VirusBatch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('virus_type', models.CharField(blank=True, help_text='UPenn ID or equivalent', max_length=255)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('date_time_made', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('nominal_titer', models.FloatField(blank=True, help_text='TODO: What unit?', null=True)),
            ],
            options={
                'verbose_name_plural': 'virus batches',
            },
        ),
        migrations.CreateModel(
            name='Amplifier',
            fields=[
                ('appliance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Appliance')),
            ],
            options={
                'abstract': False,
            },
            bases=('equipment.appliance',),
        ),
        migrations.CreateModel(
            name='DAQ',
            fields=[
                ('appliance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Appliance')),
            ],
            options={
                'abstract': False,
            },
            bases=('equipment.appliance',),
        ),
        migrations.CreateModel(
            name='EquipmentManufacturer',
            fields=[
                ('supplier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Supplier')),
            ],
            options={
                'abstract': False,
            },
            bases=('equipment.supplier',),
        ),
        migrations.CreateModel(
            name='ExtracellularProbe',
            fields=[
                ('appliance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Appliance')),
                ('prb', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='A JSON string describing the probe connectivity and geometry. For details, see https://github.com/klusta-team/kwiklib/wiki/Kwik-format#prb', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('equipment.appliance',),
        ),
        migrations.CreateModel(
            name='LightSource',
            fields=[
                ('appliance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Appliance')),
            ],
            options={
                'abstract': False,
            },
            bases=('equipment.appliance',),
        ),
        migrations.CreateModel(
            name='PipettePuller',
            fields=[
                ('appliance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Appliance')),
            ],
            options={
                'abstract': False,
            },
            bases=('equipment.appliance',),
        ),
        migrations.CreateModel(
            name='VirusSource',
            fields=[
                ('supplier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Supplier')),
            ],
            options={
                'abstract': False,
            },
            bases=('equipment.supplier',),
        ),
        migrations.CreateModel(
            name='WeighingScale',
            fields=[
                ('appliance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Appliance')),
            ],
            options={
                'abstract': False,
            },
            bases=('equipment.appliance',),
        ),
        migrations.AddField(
            model_name='supplier',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_equipment.supplier_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='appliance',
            name='equipment_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.EquipmentModel'),
        ),
        migrations.AddField(
            model_name='appliance',
            name='location',
            field=models.ForeignKey(blank=True, help_text='The physical location of the appliance.', null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.LabLocation'),
        ),
        migrations.AddField(
            model_name='appliance',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_equipment.appliance_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='virusbatch',
            name='virus_source',
            field=models.ForeignKey(blank=True, help_text='Who supplied the virus', null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.VirusSource'),
        ),
        migrations.AddField(
            model_name='equipmentmodel',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.EquipmentManufacturer'),
        ),
    ]

# Generated by Django 2.1.4 on 2019-07-31 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20190315_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='file_size',
            field=models.BigIntegerField(blank=True, help_text='Size in bytes', null=True),
        ),
    ]

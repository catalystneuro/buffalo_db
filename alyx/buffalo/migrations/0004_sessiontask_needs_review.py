# Generated by Django 3.0.5 on 2020-06-15 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buffalo', '0003_auto_20200613_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessiontask',
            name='needs_review',
            field=models.BooleanField(default=False),
        ),
    ]
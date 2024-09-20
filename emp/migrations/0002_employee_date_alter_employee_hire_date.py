# Generated by Django 5.0.8 on 2024-09-20 04:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='date',
            field=models.TimeField(default=datetime.time(9, 0)),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hire_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]

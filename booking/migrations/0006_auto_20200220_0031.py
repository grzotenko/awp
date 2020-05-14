# Generated by Django 2.2.6 on 2020-02-19 21:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20200219_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=50, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='phone',
            field=models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='time_end',
            field=models.TimeField(default=datetime.datetime.now, verbose_name='Окончание'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='time_start',
            field=models.TimeField(default=datetime.datetime.now, verbose_name='Начало'),
        ),
    ]

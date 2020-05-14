# Generated by Django 2.2.6 on 2020-01-09 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycalendar', '0004_day_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='is_print',
            field=models.BooleanField(default=False, verbose_name='Принтер подключен'),
        ),
        migrations.AddField(
            model_name='setting',
            name='network',
            field=models.CharField(default='', max_length=50, verbose_name='Network'),
        ),
    ]

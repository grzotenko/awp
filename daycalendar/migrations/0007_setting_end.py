# Generated by Django 2.2.6 on 2020-03-18 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycalendar', '0006_setting_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='end',
            field=models.TimeField(default=None, null=True, verbose_name='Обычное время начала смены'),
        ),
    ]

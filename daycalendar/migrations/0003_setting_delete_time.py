# Generated by Django 2.2.6 on 2020-01-01 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycalendar', '0002_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='delete_time',
            field=models.PositiveIntegerField(default=10, verbose_name='Кол-во минут, при котором можно удалить посетителя'),
        ),
    ]

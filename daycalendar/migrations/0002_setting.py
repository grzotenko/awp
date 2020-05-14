# Generated by Django 2.2.6 on 2019-12-28 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daycalendar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_now', models.IntegerField(blank=True, default=0, verbose_name='Сейчас в кассе')),
            ],
            options={
                'verbose_name': 'Настройки',
                'verbose_name_plural': 'Настройки',
            },
        ),
    ]

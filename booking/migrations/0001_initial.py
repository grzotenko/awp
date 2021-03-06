# Generated by Django 2.2.6 on 2020-01-27 19:22

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0006_auto_20200108_2257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата брони')),
                ('time_start', models.TimeField(default=datetime.datetime.now, verbose_name='Начало брони')),
                ('time_end', models.TimeField(default=datetime.datetime.now, verbose_name='Окончание брони')),
                ('persons', models.PositiveSmallIntegerField(default=0, verbose_name='Кол-во человек')),
                ('text', models.CharField(blank=True, default='', max_length=1500, verbose_name='Текстовый комментарий')),
                ('name', models.CharField(blank=True, default=None, max_length=50, verbose_name='Имя клиента')),
                ('phone', models.CharField(blank=True, default=None, max_length=15, null=True, verbose_name='Телефон клиента')),
                ('dep_card', models.IntegerField(blank=True, default=0, verbose_name='Депозит картой')),
                ('dep_cash', models.IntegerField(blank=True, default=0, verbose_name='Депозит наличными')),
                ('includes', models.ManyToManyField(blank=True, to='main.IncludeService', verbose_name='Включенные в стоимость услуги')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Room', verbose_name='Занятая комната')),
                ('services', models.ManyToManyField(blank=True, to='main.AddService', verbose_name='Платные услуги')),
                ('tariff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Tariff', verbose_name='Тариф')),
            ],
            options={
                'verbose_name': 'Бронь',
                'verbose_name_plural': 'Брони',
            },
        ),
    ]

# Generated by Django 2.2.6 on 2019-12-27 15:55

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import enter.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('daycalendar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=300, unique=True, verbose_name='Названия услуг')),
                ('price', models.PositiveSmallIntegerField(default=0, verbose_name='Стоимость услуги в рублях')),
            ],
            options={
                'verbose_name_plural': 'Платные услуги',
                'verbose_name': 'Платная услуга',
            },
        ),
        migrations.CreateModel(
            name='CardPay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=0, verbose_name='Оплата картой')),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Время оплаты')),
                ('is_payed', models.BooleanField(default=False, verbose_name='Учтено в ордере Выручки')),
            ],
            options={
                'verbose_name_plural': 'Оплаты картой',
                'verbose_name': 'Оплата картой',
            },
        ),
        migrations.CreateModel(
            name='CashPay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=0, verbose_name='Оплата наличными')),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Время оплаты')),
                ('is_payed', models.BooleanField(default=False, verbose_name='Учтено в ордере Выручки')),
            ],
            options={
                'verbose_name_plural': 'Оплаты наличными',
                'verbose_name': 'Оплата наличными',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CID', models.IntegerField(verbose_name='CID')),
                ('count', models.IntegerField(blank=True, default=0, verbose_name='Общее кол-во человек')),
                ('payed', models.IntegerField(blank=True, default=0, verbose_name='Кол-во оплаченных человек')),
            ],
            options={
                'verbose_name_plural': 'Компании',
                'verbose_name': 'Компания',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, unique=True, verbose_name='Название скидки')),
                ('multiplier', models.DecimalField(decimal_places=2, default=1.0, max_digits=3, verbose_name='Множитель')),
                ('limit_gt', models.PositiveSmallIntegerField(default=2, verbose_name='Минимальное Кол-во людей')),
                ('limit_lt', models.PositiveSmallIntegerField(default=2, verbose_name='Максимальное Кол-во людей')),
                ('free', models.PositiveSmallIntegerField(default=1, verbose_name='Кол-во людей бесплатно')),
                ('days', models.ManyToManyField(blank=True, to='daycalendar.Day', verbose_name='Дни недели')),
            ],
            options={
                'verbose_name_plural': 'Скидки',
                'verbose_name': 'Скидки',
            },
        ),
        migrations.CreateModel(
            name='IncludeService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=300, unique=True, verbose_name='Названия услуг')),
            ],
            options={
                'verbose_name_plural': 'Включенные в стоимость услуги',
                'verbose_name': 'Включенная в стоимость услугу',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, unique=True, verbose_name='Названия комнаты')),
                ('color', enter.fields.ColorField(default='#FF0000', max_length=7, verbose_name='Цвет комнаты')),
                ('font', enter.fields.ColorField(default='#FFFFFF', max_length=7, verbose_name='Цвет шрифта')),
                ('capasity', models.PositiveSmallIntegerField(default=1, verbose_name='Вместимость')),
            ],
            options={
                'verbose_name_plural': 'Комнаты',
                'verbose_name': 'Комната',
            },
        ),
        migrations.CreateModel(
            name='UseService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='Кол-во')),
                ('add', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.AddService', verbose_name='Услуга')),
            ],
            options={
                'verbose_name_plural': 'Оказанные услуги',
                'verbose_name': 'Оказанная услуга',
            },
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=135, unique=True, verbose_name='Названия тарифа')),
                ('type', models.CharField(choices=[('tp', 'Повременная оплата'), ('fp', 'Фиксированный прайс')], default='Повременная оплата', max_length=25, verbose_name='Тип')),
                ('price', models.PositiveSmallIntegerField(default=0, verbose_name='Цена минуты')),
                ('fix', models.PositiveSmallIntegerField(default=0, verbose_name='Фиксированная цена')),
                ('limit', models.PositiveSmallIntegerField(default=1, verbose_name='Минимальное кол-во людей')),
                ('free', models.PositiveSmallIntegerField(default=0, verbose_name='Кол-во людей бесплатно')),
                ('time', models.TimeField(blank=True, default=datetime.time(0, 0), null=True, verbose_name='Ограничение по времени')),
                ('days', models.ManyToManyField(blank=True, to='daycalendar.Day', verbose_name='Дни недели')),
                ('discounts', models.ManyToManyField(blank=True, to='main.Discount', verbose_name='Возможные скидки при данном тарифе')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SID', models.IntegerField(verbose_name='SID')),
                ('start_dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Начало сеанса')),
                ('end_dt', models.DateTimeField(blank=True, null=True, verbose_name='Окончание сеанса')),
                ('sum', models.IntegerField(blank=True, default=0, null=True, verbose_name='Чек-лист')),
                ('is_active', models.BooleanField(default=True, verbose_name='Пользователь активен')),
                ('text', models.CharField(blank=True, default='', max_length=1500, verbose_name='Текстовый комментарий')),
                ('dep_card', models.IntegerField(blank=True, default=0, verbose_name='Депозит картой')),
                ('dep_cash', models.IntegerField(blank=True, default=0, verbose_name='Депозит наличными')),
                ('card', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='main.CardPay', verbose_name='Безнал')),
                ('cash', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='main.CashPay', verbose_name='Наличные')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Company', verbose_name='Компания')),
                ('includes', models.ManyToManyField(blank=True, to='main.IncludeService', verbose_name='Включенные в стоимость услуги')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Room', verbose_name='Занятая комната')),
                ('services', models.ManyToManyField(blank=True, to='main.UseService', verbose_name='Оказанные услуги')),
            ],
            options={
                'verbose_name_plural': 'Сессии',
                'verbose_name': 'Сессия',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Discount', verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='company',
            name='tariff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Tariff', verbose_name='Тариф'),
        ),
    ]
# Generated by Django 2.2.6 on 2020-04-07 09:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0004_profile_reserved'),
        ('management', '0002_weekend'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoneyOperations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('I', 'Приход'), ('E', 'Расход')], default='Расход', max_length=10, verbose_name='Тип операции')),
                ('name', models.CharField(default='', max_length=40, verbose_name='Название денежной операции')),
                ('is_one', models.BooleanField(default=False, verbose_name='Без подтипов')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Скрытая операция')),
                ('is_adminpay', models.BooleanField(default=False, verbose_name='Зарплата работников')),
                ('is_readonlyamount', models.BooleanField(default=False, verbose_name='Автоматическое формирование выплаты ордера')),
                ('is_revenue', models.BooleanField(default=False, verbose_name='Выручка')),
            ],
            options={
                'verbose_name_plural': 'Категории Ордеров',
                'verbose_name': 'Категория Ордеров',
            },
        ),
        migrations.CreateModel(
            name='TypeOfMO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='Подтип операции')),
                ('moneyoper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.MoneyOperations', verbose_name='Категория')),
            ],
            options={
                'verbose_name_plural': 'Подкатегории Ордеров',
                'verbose_name': 'Подкатегория Ордеров',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время операции')),
                ('amount', models.IntegerField(blank=True, default=0, verbose_name='Сумма')),
                ('comment', models.CharField(blank=True, default='', max_length=150, verbose_name='Комментарий')),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='enter.Profile', verbose_name='Админ')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.TypeOfMO', verbose_name='Выберите подтип ордера')),
            ],
            options={
                'verbose_name_plural': 'Ордеры',
                'verbose_name': 'Ордер',
            },
        ),
    ]
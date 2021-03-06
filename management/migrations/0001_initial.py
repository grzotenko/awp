# Generated by Django 2.2.6 on 2020-03-18 10:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enter', '0004_profile_reserved'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSalary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_type', models.CharField(choices=[('Рабочая смена', 'Смена'), ('Сверхурочно', 'Сверхурочно')], max_length=20, verbose_name='Тип записи')),
                ('start', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Время начальное')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='Время конечное')),
                ('comment', models.CharField(blank=True, default='', max_length=25, null=True, verbose_name='Коммент')),
                ('base', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, verbose_name='Сумма базовая')),
                ('bonus', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, verbose_name='Сумма бонусная')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, verbose_name='Количество')),
                ('is_payed', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('payedProcent', models.SmallIntegerField(default=0, verbose_name='Невыплаченные деньги')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='enter.Profile', verbose_name='Администратор')),
            ],
            options={
                'verbose_name_plural': 'Зарплатные начисления',
                'verbose_name': 'Зарплатное начисление',
            },
        ),
    ]

# Generated by Django 2.2.6 on 2020-04-10 09:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0004_profile_reserved'),
        ('management', '0005_preferences_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='PremiumFine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('type', models.CharField(choices=[('P', 'Премия'), ('F', 'Штраф')], max_length=20, verbose_name='Тип записи')),
                ('amount', models.IntegerField(blank=True, default=0, verbose_name='Сумма')),
                ('is_payed', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('comment', models.CharField(blank=True, default='', max_length=125, null=True, verbose_name='Коммент')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='enter.Profile', verbose_name='Администратор')),
            ],
            options={
                'verbose_name': 'Премии/Штрафы',
                'verbose_name_plural': 'Премии/Штрафы',
            },
        ),
    ]

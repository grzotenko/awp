# Generated by Django 2.2.6 on 2020-07-25 08:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_title', models.CharField(default='', max_length=20, verbose_name='Название категории')),
            ],
            options={
                'verbose_name_plural': 'Категории',
                'verbose_name': 'Категория',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=20, verbose_name='Название расходника')),
                ('yellow', models.FloatField(default=0, verbose_name='Желтый уровень')),
                ('red', models.FloatField(default=0, verbose_name='Красный уровень')),
            ],
            options={
                'verbose_name_plural': 'Товары',
                'verbose_name': 'Товар',
            },
        ),
        migrations.CreateModel(
            name='WhatsApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_sid', models.CharField(default='', max_length=50, verbose_name='SID')),
                ('auth_token', models.CharField(default='', max_length=50, verbose_name='Токен')),
                ('send_to', models.CharField(default='', max_length=20, verbose_name='Номер получателя')),
                ('send_from', models.CharField(default='', max_length=20, verbose_name='Номер отправителя')),
            ],
            options={
                'verbose_name_plural': 'WhatsApp',
                'verbose_name': 'WhatsApp',
            },
        ),
        migrations.CreateModel(
            name='WarehouseInOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата операции')),
                ('type_operations', models.CharField(choices=[('Приход', 'Приход'), ('Расход', 'Расход')], default='Приход', max_length=20, verbose_name='Тип операции')),
                ('volume', models.FloatField(default=0, verbose_name='Объем упаковки')),
                ('amount', models.FloatField(default=0, verbose_name='Кол-во упаковок')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Потрачено денег')),
                ('comment', models.CharField(blank=True, default='', max_length=30, verbose_name='Комментарий')),
                ('title_goods', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='warehouse.Goods', verbose_name='Товар')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
            options={
                'verbose_name_plural': 'Движения на складе',
                'verbose_name': 'Движение на складе',
            },
        ),
        migrations.CreateModel(
            name='Volumes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.FloatField(default=0, verbose_name='Объем упаковки')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='Кол-во упаковок')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Goods', verbose_name='Товар')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcat_title', models.CharField(default='', max_length=20, verbose_name='Название подкатегории')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='warehouse.Categories', verbose_name='Категория')),
            ],
            options={
                'verbose_name_plural': 'Подкатегории',
                'verbose_name': 'Подкатегория ',
            },
        ),
        migrations.AddField(
            model_name='goods',
            name='subcat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='warehouse.Subcategories', verbose_name='Подкатегория товара'),
        ),
        migrations.CreateModel(
            name='Costs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0, verbose_name='Количество единиц товара')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('good', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='warehouse.Goods', verbose_name='Товар')),
            ],
        ),
    ]

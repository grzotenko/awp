# Generated by Django 2.2.6 on 2020-04-14 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_premiumfine'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currentplan',
            options={'ordering': ['day'], 'verbose_name': 'Текущий план смен', 'verbose_name_plural': 'Текущий план смен'},
        ),
        migrations.AlterModelOptions(
            name='futureplan',
            options={'ordering': ['day'], 'verbose_name': 'План смен на следующую неделю', 'verbose_name_plural': 'План смен на следующую неделю'},
        ),
    ]

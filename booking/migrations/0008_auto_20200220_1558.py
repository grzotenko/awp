# Generated by Django 2.2.6 on 2020-02-20 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_booking_discount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='discount',
            new_name='discountB',
        ),
    ]

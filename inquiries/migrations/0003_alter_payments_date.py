# Generated by Django 3.2.9 on 2021-11-05 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0002_alter_payments_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 11, 5, 13, 56, 54, 840429), verbose_name='Date'),
        ),
    ]
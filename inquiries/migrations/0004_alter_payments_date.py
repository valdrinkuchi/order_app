# Generated by Django 3.2.9 on 2021-11-05 14:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0003_alter_payments_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 11, 5, 14, 1, 4, 787660), verbose_name='Date'),
        ),
    ]

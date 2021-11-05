# Generated by Django 3.2.9 on 2021-11-05 13:09

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import inquiries.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=200, unique=True, verbose_name='Brand Name')),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_number', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=1024, unique=True, verbose_name='Short Name')),
                ('full_name', models.CharField(blank=True, max_length=1024, unique=True, verbose_name='Complete Name')),
                ('address', models.CharField(max_length=1024)),
                ('city', models.CharField(blank=True, max_length=20)),
                ('delivery_address', models.CharField(max_length=1024)),
                ('delivery_address_2', models.CharField(blank=True, max_length=1024)),
                ('postal_code', models.CharField(max_length=12)),
                ('country', models.CharField(max_length=8)),
                ('bonus', models.FloatField(blank=True, default=0, null=True, verbose_name='Bonus')),
            ],
        ),
        migrations.CreateModel(
            name='IncomingInvoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=120, verbose_name='Inovice Number')),
                ('invoice_date', models.DateField(verbose_name='Invoice Date')),
                ('invoice_type', models.CharField(choices=[('Invoice', 'Invoice'), ('Reklamation', 'Reklamation'), ('Diverse', 'Diverse')], max_length=1024, null=True)),
                ('closed', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.customers')),
            ],
        ),
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=120, unique=True, verbose_name='Inovice Number')),
                ('invoice_date', models.DateField(verbose_name='Invoice Date')),
                ('invoice_type', models.CharField(choices=[('Invoice', 'Invoice'), ('Reklamation', 'Reklamation'), ('Diverse', 'Diverse')], max_length=1024)),
                ('cancelled', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.customers')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=8, unique=True, verbose_name='Order Number')),
                ('article', models.CharField(max_length=12, verbose_name='Article')),
                ('date', models.DateField(verbose_name='Signed Date')),
                ('order_due_date', models.DateField(verbose_name='Delivery Date')),
                ('order_pcs', models.IntegerField(verbose_name='Total Pieces')),
                ('price', models.FloatField(verbose_name='Price')),
                ('in_production', models.BooleanField(default=False)),
                ('description', models.CharField(blank=True, max_length=120, null=True, verbose_name='Description')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.brands')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.customers')),
            ],
        ),
        migrations.CreateModel(
            name='Producers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producer_number', models.CharField(max_length=200, unique=True, verbose_name='Producer Number')),
                ('name', models.CharField(max_length=1024, unique=True, verbose_name='Short Name')),
                ('full_name', models.CharField(blank=True, max_length=1024, unique=True, verbose_name='Complete Name')),
                ('address', models.CharField(max_length=1024, unique=True, verbose_name='Address')),
                ('city', models.CharField(blank=True, max_length=20)),
                ('country', models.CharField(max_length=8, verbose_name='Country')),
            ],
        ),
        migrations.CreateModel(
            name='Productions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('production_due_date', models.DateField(null=True, verbose_name='Confirmed Date')),
                ('load_date', models.DateField(blank=True, null=True, verbose_name='Load Date')),
                ('production_load_count', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Amount(pcs)')),
                ('production_price', models.FloatField(null=True, verbose_name='Production Price')),
                ('bonus', models.FloatField(blank=True, default=4, null=True)),
                ('assigned_in_invoice', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('in_invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.incominginvoices')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inquiries.invoices')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inquiries.orders', verbose_name='Order Number')),
                ('producer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.producers')),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0, verbose_name='Amount')),
                ('date', models.DateField(default=datetime.datetime(2021, 11, 5, 13, 9, 36, 406476), verbose_name='Date')),
                ('payment_type', models.TextField(choices=[('In', 'Incoming'), ('Out', 'Outgoing')], max_length=1024, null=True)),
                ('description', models.CharField(blank=True, max_length=120, null=True, verbose_name='Description')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.customers')),
                ('producer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.producers')),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Item name')),
                ('description', models.CharField(blank=True, max_length=120, null=True, verbose_name='Item description')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Price')),
                ('amount', models.IntegerField(blank=True, null=True, verbose_name='Amount')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='Total')),
                ('vat', models.FloatField(blank=True, null=True, verbose_name='Vat')),
                ('total_sum', models.FloatField(blank=True, null=True, verbose_name='Total Sum')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.customers')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inquiries.invoices')),
                ('producer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.producers')),
            ],
        ),
        migrations.AddField(
            model_name='invoices',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.payments', verbose_name='Payment'),
        ),
        migrations.AddField(
            model_name='invoices',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.producers'),
        ),
        migrations.AddField(
            model_name='incominginvoices',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.payments', verbose_name='Payment'),
        ),
        migrations.AddField(
            model_name='incominginvoices',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inquiries.producers'),
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='', validators=[inquiries.validators.validate_file_size])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inquiries.incominginvoices', verbose_name='Invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Calculations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True, verbose_name='Loaded Date')),
                ('sale_neto', models.FloatField(blank=True, verbose_name='Neto Sum')),
                ('sale_vat', models.FloatField(blank=True, verbose_name='Total VAT')),
                ('sale_gross', models.FloatField(blank=True, verbose_name='Gross Sum')),
                ('buy_neto', models.FloatField(blank=True, default=0, verbose_name='Neto Sum')),
                ('buy_bonus', models.FloatField(blank=True, default=0, verbose_name='Total Bonus')),
                ('buy_gross', models.FloatField(blank=True, default=0, verbose_name='Buy Gross')),
                ('profit', models.FloatField(blank=True, default=0, verbose_name='Profit')),
                ('days_late', models.IntegerField(blank=True, default=0, verbose_name='Late Delivery')),
                ('amount_difference', models.IntegerField(blank=True, verbose_name='Amount Difference')),
                ('description', models.CharField(blank=True, max_length=20, null=True, verbose_name='Item Description')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inquiries.orders', verbose_name='Order Number')),
                ('production', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inquiries.productions', verbose_name='Production')),
            ],
        ),
        migrations.AddField(
            model_name='brands',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inquiries.customers', verbose_name='Customer ID'),
        ),
    ]

from django.db import models

from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import validate_file_size
# Create your models here.

class Customers(models.Model):
    customer_number = models.IntegerField(unique=True, blank =False,)
    name = models.CharField(unique=True, blank =False,max_length=1024,verbose_name= 'Short Name')
    full_name = models.CharField(unique=True, blank =True, max_length=1024,verbose_name= 'Complete Name')
    address = models.CharField(max_length=1024,)
    city = models.CharField(max_length=20,blank =True,)
    delivery_address = models.CharField(max_length=1024,)
    delivery_address_2 = models.CharField(max_length=1024,blank=True,)
    postal_code = models.CharField(max_length=12,)
    country = models.CharField(max_length=8,)
    bonus = models.FloatField(blank =True,default=0,null=True,verbose_name="Bonus")

    def __str__(self):
        return '{}'.format(self.name)

class Producers(models.Model):
    producer_number = models.CharField(unique=True,max_length=200,verbose_name= 'Producer Number')
    name = models.CharField(unique=True, blank =False, max_length=1024,verbose_name= 'Short Name')
    full_name = models.CharField(unique=True, blank =True, max_length=1024,verbose_name= 'Complete Name')
    address = models.CharField(unique=True, blank =False,max_length=1024,verbose_name= 'Address')
    city = models.CharField(max_length=20,blank =True,)
    country = models.CharField(max_length=8,verbose_name= 'Country')


    def __str__(self):
        return '{}'.format(self.name)


class Orders(models.Model):
    order_number = models.CharField(unique=True, blank =False,max_length=8,verbose_name="Order Number")
    article = models.CharField(max_length=12,blank =False,verbose_name="Article")
    date = models.DateField( blank =False,verbose_name="Signed Date",)
    order_due_date = models.DateField(blank =False,verbose_name="Delivery Date")
    order_pcs = models.IntegerField(blank =False,verbose_name="Total Pieces")
    customer = models.ForeignKey('Customers',null=True, on_delete = models.SET_NULL,)
    price = models.FloatField(verbose_name="Price")
    brand = models.ForeignKey('Brands',null=True, on_delete = models.SET_NULL)
    in_production = models.BooleanField(default=False)
    description = models.CharField(max_length=120,blank =True,null=True,verbose_name="Description")

    def __str__(self):
        return '{}'.format(self.order_number)

class Productions(models.Model):
    order = models.ForeignKey('Orders',on_delete=models.CASCADE,verbose_name="Order Number")
    production_due_date = models.DateField(null=True,verbose_name="Confirmed Date")
    load_date = models.DateField(blank=True,null=True,verbose_name="Load Date")
    producer = models.ForeignKey('Producers',null=True,on_delete=models.SET_NULL)
    production_load_count = models.IntegerField(blank =False,null=True,validators=[MinValueValidator(1)],verbose_name="Amount(pcs)")
    production_price = models.FloatField(blank =False,null=True,verbose_name="Production Price")
    bonus = models.FloatField(blank=True,null=True, default=4,)
    assigned_in_invoice = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    in_invoice = models.ForeignKey('IncomingInvoices',blank=True,null=True,on_delete = models.SET_NULL)
    invoice = models.ForeignKey('Invoices',blank=True,null=True,on_delete = models.CASCADE)

    def __str__(self):
        return '{}'.format(self.order)

class Calculations(models.Model):
    order = models.ForeignKey('Orders',on_delete=models.CASCADE,verbose_name="Order Number", null = True)
    production = models.ForeignKey('Productions',on_delete=models.CASCADE,verbose_name="Production", null=True)
    date = models.DateField(blank=False,null=True,verbose_name="Loaded Date")
    sale_neto = models.FloatField(blank =True,verbose_name="Neto Sum")
    sale_vat = models.FloatField(blank =True,verbose_name="Total VAT")
    sale_gross = models.FloatField(blank =True,verbose_name="Gross Sum")
    buy_neto = models.FloatField(blank =True,default=0,verbose_name="Neto Sum")
    buy_bonus = models.FloatField(blank =True,default=0,verbose_name="Total Bonus")
    buy_gross = models.FloatField(blank =True,default=0,verbose_name="Buy Gross")
    profit = models.FloatField(blank =True,default=0,verbose_name="Profit")
    days_late = models.IntegerField(blank =True,default=0,verbose_name="Late Delivery")
    amount_difference = models.IntegerField(blank =True,verbose_name="Amount Difference")
    description = models.CharField(max_length=20,blank=True,null=True,verbose_name="Item Description")

    def __str__(self):
        return '{}'.format(self.order)

class Brands(models.Model):
    brand_name = models.CharField(unique=True, blank =False,max_length=200,verbose_name= 'Brand Name')
    customer = models.ForeignKey('Customers',on_delete=models.CASCADE,verbose_name= 'Customer ID')

    def __str__(self):
        return '{} - {}'.format(self.brand_name,self.customer)

class Payments(models.Model):
    PAYMENT_TYPE = [
        ('In', 'Incoming'),
        ('Out', 'Outgoing'),
    ]
    amount = models.FloatField(blank=False,default=0,verbose_name="Amount")
    date = models.DateField(default=datetime.datetime.now(), blank =False,verbose_name="Date")
    customer = models.ForeignKey('Customers',blank=True,null=True,on_delete = models.SET_NULL)
    producer = models.ForeignKey('Producers',blank=True,null=True,on_delete = models.SET_NULL)
    payment_type = models.TextField(blank =False,null=True, max_length=1024,choices= PAYMENT_TYPE)
    description = models.CharField(max_length=120,blank=True,null=True,verbose_name="Description")

    def __str__(self):
        return '{} - {} - {}'.format(self.date,self.amount, self.payment_type)

class Invoices(models.Model):
    INVOICE_TYPE = [
        ('Invoice', 'Invoice'),
        ('Reklamation', 'Reklamation'),
        ('Diverse','Diverse'),
    ]
    invoice_number = models.CharField(max_length=120,unique=True, blank =False,verbose_name="Inovice Number")
    invoice_date = models.DateField(blank =False,verbose_name="Invoice Date")
    customer = models.ForeignKey('Customers',blank=True,null=True,on_delete = models.SET_NULL)
    producer = models.ForeignKey('Producers',blank=True,null=True,on_delete = models.SET_NULL)
    invoice_type = models.CharField(blank =False, max_length=1024,choices=INVOICE_TYPE)
    payment = models.ForeignKey('Payments',blank=True,null=True,on_delete=models.SET_NULL,verbose_name="Payment")
    cancelled = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.invoice_number)

class IncomingInvoices(models.Model):
    INVOICE_TYPE = [
        ('Invoice', 'Invoice'),
        ('Reklamation', 'Reklamation'),
        ('Diverse','Diverse')
    ]
    invoice_number = models.CharField(max_length=120,blank =False,verbose_name="Inovice Number")
    invoice_date = models.DateField(blank =False,verbose_name="Invoice Date")
    customer = models.ForeignKey('Customers',blank=True,null=True,on_delete = models.SET_NULL)
    producer = models.ForeignKey('Producers',blank=True,null=True,on_delete = models.SET_NULL)
    invoice_type = models.CharField(blank =False,null=True, max_length=1024,choices=INVOICE_TYPE)
    payment = models.ForeignKey('Payments',blank=True,null=True,on_delete=models.SET_NULL,verbose_name="Payment")
    closed = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.invoice_number)

class Documents(models.Model):
    invoice = models.ForeignKey('IncomingInvoices',blank=True,null=True,on_delete=models.CASCADE,verbose_name="Invoice")
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(validators=[validate_file_size])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.document)

    def delete(self,*args, **kwargs):
        self.document.delete()
        super().delete(*args, **kwargs)

class Items(models.Model):
    name = models.CharField(blank=True,null=True, max_length=120,verbose_name="Item name")
    description = models.CharField(blank=True,null=True, max_length=120,verbose_name="Item description")
    customer = models.ForeignKey('Customers',blank=True,null=True,on_delete = models.SET_NULL)
    producer = models.ForeignKey('Producers',blank=True,null=True,on_delete = models.SET_NULL)
    price = models.FloatField(blank=True,null=True,verbose_name="Price")
    amount = models.IntegerField(blank=True,null=True,verbose_name="Amount")
    invoice = models.ForeignKey('Invoices',blank=True,null=True,on_delete = models.CASCADE)
    total = models.FloatField(blank=True,null=True,verbose_name="Total")
    vat = models.FloatField(blank=True,null=True,verbose_name="Vat")
    total_sum = models.FloatField(blank=True,null=True,verbose_name="Total Sum")

    def __str__(self):
        return '{}-{}-{}'.format(self.invoice.invoice_date,self.name,self.invoice)

from django.contrib import admin
from .models import *
@admin.register(Orders,Producers,Customers,Calculations,Brands,Payments,Productions,Invoices,Items,IncomingInvoices,Documents)
class Viewadmin(admin.ModelAdmin):
    pass
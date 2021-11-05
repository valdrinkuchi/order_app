from django.conf.urls import url,include
from django.urls import path
from .views.delete import *
from .views.cancel_invoice import *
from .views.edit import *
from .views.edit_production import *
from .views.display import *
from .views.add_invoice import *
from .views.add_production import *
from .views.add import *
from .views.invoice_detail import *
from .views.add_payment import *
from .views.register_invoice import *
from .views.edit_payment import *
from .views.edit_in_invoices import *
from django.contrib.auth import views as auth_views

urlpatterns =[

    path('',index,name='index'),

    path('accounting/',accounting,name='accounting'),
    path('select_customer/',select_customer,name='select_customer'),
    path('select_producer/',select_producer,name='select_producer'),
    path('order_lookup/',order_lookup,name='order_lookup'),
    path('export_customer_csv/',export_customer_csv,name='export_customer_csv'),
    path('export_producer_csv/',export_producer_csv,name='export_producer_csv'),
    path('export_customer_pdf/',export_customer_pdf,name='export_customer_pdf'),
    path('export_producer_pdf/',export_producer_pdf,name='export_producer_pdf'),
    path('export_invoice_pdf/<pk>/',export_invoice_pdf,name='export_invoice_pdf'),

    path('display_orders/',display_orders,name='display_orders'),
    path('display_brands/',display_brands,name='display_brands'),
    path('display_production/',display_production,name='display_production'),
    path('display_producers/',display_producers,name='display_producers'),
    path('display_customers/',display_customers,name='display_customers'),
    path('display_payments/',display_payments,name='display_payments'),
    path('display_invoices/',display_invoices,name='display_invoices'),
    path('incoming_invoices/',incoming_invoices,name='incoming_invoices'),

    path('invoice_detail/<pk>',invoice_detail,name='invoice_detail'),
    path('edit_in_invoice/<pk>',edit_in_invoice,name='edit_in_invoice'),

    path('add_orders/',add_orders,name='add_orders'),
    path('add_customer/',add_customer,name='add_customer'),
    path('add_producer/',add_producer,name='add_producer'),
    path('add_brands/',add_brands,name='add_brands'),
    path('add_production/',add_production,name='add_production'),
    path('add_payment/',add_payment,name='add_payment'),
    path('add_invoice/',add_invoice,name='add_invoice'),

    path('register_invoice/',register_invoice,name='register_invoice'),

    path('edit_orders/<pk>',edit_orders,name='edit_orders'),
    path('edit_customers/<pk>',edit_customers,name='edit_customers'),
    path('edit_producer/<pk>',edit_producer,name='edit_producer'),
    path('edit_brands/<pk>',edit_brands,name='edit_brands'),

    path('edit_production/<pk>',edit_production,name='edit_production'),

    path('edit_payment/<pk>',edit_payment,name='edit_payment'),

    path('delete_orders/<pk>',delete_orders,name='delete_orders'),
    path('delete_customers/<pk>',delete_customers,name='delete_customers'),
    path('delete_producer/<pk>',delete_producer,name='delete_producer'),
    path('delete_brands/<pk>',delete_brands,name='delete_brands'),
    path('delete_production/<pk>',delete_production,name='delete_production'),
    path('delete_payment/<pk>',delete_payment,name='delete_payment'),
    path('delete_in_invoice/<pk>',delete_in_invoice,name='delete_in_invoice'),
    path('cancel_invoice/<pk>',cancel_invoice,name='cancel_invoice'),

]

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from inquiries.models import *
from inquiries.forms import *
from inquiries.functions import create_calculation, edit_calculation
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def is_edit_valid(request,form,pk):
    is_valid = True

    if isinstance(form, BrandsForm):
        new_brand_name = form['brand_name'].data
        current_brand = Brands.objects.get(pk=pk).brand_name
        if new_brand_name != current_brand:
            already_existing_brand = Brands.objects.filter(brand_name=new_brand_name)

            if already_existing_brand:
                is_valid = False
                messages.warning(request, "Brand name already exists")
    if isinstance(form,PaymentForm):
        customer = form['customer'].data
        producer = form['producer'].data
        if customer and producer:
            is_valid = False
            messages.warning(request, "One Payment cannot be assigned both for Customer and Producer!")

    if isinstance(form, ProductionForm):
        new_order_number = form['order'].data
        order_signed_date = Orders.objects.get(order_id=new_order_number).date
        confirmed_date = datetime.strptime(form['production_due_date'].data, '%Y-%m-%d').date()
        load_count = form['production_load_count'].data
        invoice = form['in_invoice'].data
        c = int(load_count)
        price = float(form['production_price'].data)
        load_date = form['load_date'].data
        order_producer = Orders.objects.get(pk=new_order_number).producer
        if price < 0:
            is_valid = False
            messages.warning(request, "Price cannot be negative!")

        if (not load_count and load_date and invoice) or (not load_date and load_count and invoice) or (not invoice and load_count and load_date) or (invoice and not load_count and not load_date) or (not invoice and load_count and not load_date) or (not invoice and not load_count and load_date):
            is_valid = False
            messages.warning(request,"Amount,Load Date or Invoice Number Error. Please check these fields!")

        if order_signed_date >= confirmed_date:
            is_valid = False
            messages.warning(request, "Delivery date can not be earlier than signed date!")

        if load_date:
            load_date = datetime.strptime(form['load_date'].data, '%Y-%m-%d').date()
            if order_signed_date >= load_date:
                is_valid = False
                messages.warning(request, "Loading date can not be earlier than signed date!")
        if invoice:
            if IncomingInvoices.objects.get(pk=invoice):
                invoice_producer = IncomingInvoices.objects.get(pk=invoice).producer
                if invoice_producer != order_producer:
                    is_valid = False
                    messages.warning(request, "This Order doesn't belond to this Producer!")

    if isinstance(form, OrdersForm):
        new_order_number = form['order_number'].data
        date_obj = datetime.strptime(form['date'].data, '%Y-%m-%d')
        due_date_obj = datetime.strptime(form['order_due_date'].data, '%Y-%m-%d')
        order_price = form['price'].data
        p = float(order_price)
        order_pcs = form['order_pcs'].data
        if int(order_pcs) <0:
            is_valid = False
            messages.warning(request, "Total Pieces cannot be a negative number!")
        if p < 0:
            is_valid = False
            messages.warning(request, "Price cannot be negative!")
        if date_obj > due_date_obj:
            is_valid = False
            messages.warning(request, "Please check the delivery date")
        b = form['brand'].data
        c = form['customer'].data
        if int(c) != (Brands.objects.get(pk=b)).customer.pk:
            is_valid = False
            messages.warning(request, "Please check customer and brand")
    return is_valid

@login_required
def edit_info(request,pk,model,cls,template, delete_url,context):
    info = get_object_or_404(model, pk=pk)
    if request.method =='POST':
        form = cls(request.POST, instance=info)
        if (context == 'Order') and not is_edit_valid(request, form,pk):
            return render(request,'edit_info.html',{'form': form,'template':template, 'Model': info, 'delete_url': delete_url})
        if (context=='Brand') and not is_edit_valid(request, form,pk):
            return render(request,'edit_info.html',{'form': form,'template':template, 'Model': info, 'delete_url': delete_url})
        if form.is_valid():
            obj = form
            if (context == 'Order'):
                calculation_test = Calculations.objects.filter(order=pk)
                if calculation_test:
                    obj.save()
                    edit_calculation(form).save()
                    messages.success(request, 'Order' + " succesfully edited")
                    return redirect(template)
            obj.save()
            messages.success(request, context + " succesfully edited")
            return redirect(template)
    else:
        form = cls(instance=info)
        return render(request, 'edit_info.html', {'form': form,'template':template, 'Model': info, 'delete_url': delete_url})



def edit_orders(request,pk):
    return edit_info(request,pk,Orders,OrdersForm,'display_orders', 'delete_orders','Order')

def edit_customers(request,pk):
    return edit_info(request,pk, Customers, CustomersForm,'display_customers', 'delete_customers','Customer')

def edit_producer(request,pk):
    return edit_info(request,pk, Producers, ProducerForm,'display_producers', 'delete_producer','Producer')

def edit_brands(request,pk):
    return edit_info(request,pk, Brands, BrandsForm,'display_brands', 'delete_brands','Brand')







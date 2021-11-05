from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from inquiries.models import *
from inquiries.forms import *
from inquiries.views.edit import edit_info
from inquiries.functions import create_calculation,add_calculation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def is_form_valid(request, form):
    is_valid = True

    if isinstance(form, BrandsForm):
        new_brand_name = form['brand_name'].data
        already_existing_brand = Brands.objects.filter(brand_name=new_brand_name)

        if already_existing_brand:
            is_valid = False
            messages.warning(request, "Brand name already exists")

    if isinstance(form, OrdersForm):
        date_obj = datetime.datetime.strptime(form['date'].data, '%Y-%m-%d')
        due_date_obj = datetime.datetime.strptime(form['order_due_date'].data, '%Y-%m-%d')
        order_price = form['price'].data
        p = float(order_price)
        order = form['order_number'].data
        order_pcs = form['order_pcs'].data
        if int(order_pcs) <0:
            is_valid = False
            messages.warning(request, "Total Pieces cannot be a negative number!")
        if Orders.objects.filter(order_number=order):
            is_valid = False
            messages.warning(request, "Order number should be unique!")
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
def add_new(request, cls, context,template):
    form = cls()
    if  request.method =='POST':
        form = cls(request.POST)
        if (context == 'Order') and not is_form_valid(request, form):
            return render(request,'add_info.html',{'form':form,'template':template})
        if (context=='Brand') and not is_form_valid(request, form):
            return render(request,'add_info.html',{'form':form,'template':template})

        if form.is_valid():
            form.save()
        messages.success(request, context + " succesfully created")
        return redirect(template)
    else:
        form = cls()
        return render(request,'add_info.html',{'form':form, 'title': context,'template':template})
@login_required
def add_orders(request):
    return add_new(request, OrdersForm, 'Order','display_orders')
@login_required
def add_customer(request):
    return add_new(request, CustomersForm, 'Customer','display_customers')
@login_required
def add_producer(request):
    return add_new(request, ProducerForm, 'Producer','display_producers')
@login_required
def add_brands(request):
    return add_new(request, BrandsForm, 'Brand','display_brands')



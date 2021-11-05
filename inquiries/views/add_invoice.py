from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from inquiries.models import *
from inquiries.forms import *
from inquiries.views.edit import edit_info
from inquiries.functions import create_calculation,add_calculation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
@login_required
def add_invoice(request):
    form = RawInvoiceForm(request.POST or None)
    if request.method =='POST':
        form = RawInvoiceForm(request.POST)
        invoice_type = form['invoice_type'].data
        number = form['invoice_number'].data
        date = datetime.strptime(form['invoice_date'].data, '%Y-%m-%d').date()
        in_production_list = request.POST.getlist('productions[]')
        item_list = request.POST.getlist('name[]')
        description_list = request.POST.getlist('description[]')
        price_list = request.POST.getlist('price[]')
        amount_list = request.POST.getlist('amount[]')
        producer = request.POST.get('producer')
        customer = request.POST.get('customer')
        if Invoices.objects.filter(invoice_number=number):
            messages.warning(request, "Invoices must have a unique number!")
            return render(request,'add_invoice.html',{'form':form,
                    'production_list': Productions.objects.filter(active=True,production_load_count__gte=1),
                    'producers_list':Producers.objects.all(),
                    'customers_list':Customers.objects.all()})

        if invoice_type =='Reklamation' and not producer or not item_list or not description_list or not amount_list or not price_list:
                messages.warning(request, "Fileds cannot be empty!")
                return render(request,'add_invoice.html',{'form':form,
                    'production_list': Productions.objects.filter(active=True,production_load_count__gte=1),
                    'producers_list':Producers.objects.all(),
                    'customers_list':Customers.objects.all()})

        if invoice_type =='Diverse' and not customer or not item_list or not description_list or not amount_list or not price_list:
                messages.warning(request, "Fileds cannot be empty!")
                return render(request,'add_invoice.html',{'form':form,
                    'production_list': Productions.objects.filter(active=True,production_load_count__gte=1),
                    'producers_list':Producers.objects.all(),
                    'customers_list':Customers.objects.all()})

        if invoice_type == 'Invoice' and not in_production_list:
                messages.warning(request, "Invoice must have an Order number assigend!")
                return render(request,'add_invoice.html',{'form':form,
                    'production_list': Productions.objects.filter(active=True,production_load_count__gte=1),
                    'producers_list':Producers.objects.all(),
                    'customers_list':Customers.objects.all()})

        if invoice_type == 'Invoice':
            for prod in in_production_list:
                load_date = Productions.objects.get(pk=prod).load_date
                if date < load_date:
                    messages.warning(request, "Invoice Date cannot be earlier than Load Date!")
                    return render(request,'add_invoice.html',{'form':form,
                    'production_list': Productions.objects.filter(active=True,production_load_count__gte=1),
                    'producers_list':Producers.objects.all(),
                    'customers_list':Customers.objects.all()})

        if invoice_type == 'Invoice' and len(in_production_list) > 1:
            order_cutomer = Productions.objects.get(pk=in_production_list[0]).order.customer
            for prod in in_production_list:
                check_customer = Productions.objects.get(pk=prod).order.customer
                if order_cutomer != check_customer:
                    messages.warning(request, "Selected Orders must belong to a single Customer!")
                    return render(request,'add_invoice.html',{'form':form,
                    'production_list': Productions.objects.filter(active=True,production_load_count__gte=1),
                    'producers_list':Producers.objects.all(),
                    'customers_list':Customers.objects.all()})

        if form.is_valid():
            if invoice_type =='Invoice'and in_production_list:
                customer_pk = Productions.objects.get(pk=in_production_list[0]).order.customer.pk
                new_invoice = Invoices(
                                invoice_type=invoice_type,
                                invoice_date=date,
                                customer = Customers.objects.get(pk=customer_pk),
                                invoice_number=number
                )
                form = new_invoice
                new_invoice.save()
                for prod in in_production_list:
                    production_obj = Productions.objects.get(pk = prod)
                    production_obj.invoice = new_invoice
                    production_obj.active = False
                    production_obj.save()
                    new_item = Items(
                            name=str(production_obj.order),
                            description=production_obj.order.description,
                            price=production_obj.order.price,
                            amount=production_obj.production_load_count,
                            customer=production_obj.order.customer,
                            invoice=new_invoice,
                            total=Calculations.objects.get(production=prod).sale_neto,
                            vat=Calculations.objects.get(production=prod).sale_vat,
                            total_sum=Calculations.objects.get(production=prod).sale_gross
                    )
                    form = new_item
                    new_item.save()

            if invoice_type =='Reklamation':
                new_invoice = Invoices(
                                invoice_type=invoice_type,
                                invoice_date=date,
                                producer = Producers.objects.get(pk=producer),
                                invoice_number=number
                )
                form = new_invoice
                new_invoice.save()
                for name,description,price,amount in zip(item_list,description_list,price_list,amount_list):
                    total_int = float(price) *int(amount)
                    total = float("{:.2f}".format(total_int))
                    vat = total*0.19
                    total_sum = total+vat
                    new_item = Items(
                        name=name,
                        description=description,
                        price=float(price),
                        amount=amount,
                        producer=Producers.objects.get(pk=producer),
                        invoice=new_invoice,
                        total=total,
                        vat=vat,
                        total_sum=total_sum
                    )
                    form = new_item
                    new_item.save()
            if invoice_type =='Diverse' and customer:
                new_invoice = Invoices(
                                invoice_type=invoice_type,
                                invoice_date=date,
                                customer = Customers.objects.get(pk=customer),
                                invoice_number=number
                )
                form = new_invoice
                new_invoice.save()
                for name,description,price,amount in zip(item_list,description_list,price_list,amount_list):
                    total = float(price) *int(amount)
                    vat = float("{:.2f}".format(total))
                    total_sum = total+vat
                    new_item = Items(
                        name=name,
                        description=description,
                        price=float(price),
                        amount=amount,
                        customer=Customers.objects.get(pk=customer),
                        invoice=new_invoice,
                        total=total,
                        vat=vat,
                        total_sum=total_sum
                    )
                    form = new_item
                    new_item.save()

            if invoice_type =='Diverse' and producer:
                new_invoice = Invoices(
                                invoice_type=invoice_type,
                                invoice_date=date,
                                producer = Producers.objects.get(pk=producer),
                                invoice_number=number
                )
                form = new_invoice
                new_invoice.save()
                for name,description,price,amount in zip(item_list,description_list,price_list,amount_list):
                    total = float(price) *int(amount)
                    vat = float("{:.2f}".format(total_int))
                    total_sum = total+vat
                    new_item = Items(
                        name=name,
                        description=description,
                        price=float(price),
                        amount=amount,
                        producer = Producers.objects.get(pk=producer),
                        invoice=new_invoice,
                        total=total,
                        vat=vat,
                        total_sum=total_sum
                    )
                    form = new_item
                    new_item.save()
                messages.success(request, 'Invoice' + " succesfully created")
                return redirect('display_invoices')
        form.save()
        messages.success(request, 'Invoice' + " succesfully created")
        return redirect('display_invoices')
    else:
        form = RawInvoiceForm()
        return render(request,'add_invoice.html',{'form':form,
                    'production_list': Productions.objects.filter(active=True,production_load_count__gte=1),
                    'producers_list':Producers.objects.all(),
                    'customers_list':Customers.objects.all()})

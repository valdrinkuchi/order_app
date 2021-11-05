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
def add_payment(request):
    form = PaymentForm()
    if  request.method =='POST':
        form = PaymentForm(request.POST)
        payment_type = request.POST.get('payment_type')
        amount = request.POST.get('amount')
        date = datetime.strptime(form['date'].data, '%Y-%m-%d').date()
        in_invoices = request.POST.getlist('in_invoices[]')
        out_invoices = request.POST.getlist('out_invoices[]')
        description = request.POST.get('description')
        producer = request.POST.get('producer')
        customer = request.POST.get('customer')
        if payment_type == "In" and not out_invoices and not customer:
                messages.warning(request,"Payment should be assigned to an Invoice and a Customer")
                return render(request,'add_payment.html',{'form':form,
                    'customers_list':Customers.objects.all(),
                    'producers_list':Producers.objects.all(),
                    'in_invoices':Invoices.objects.filter(cancelled=False,payment__isnull=True),
                    'out_invoices':IncomingInvoices.objects.filter(closed=False)})
        if payment_type == "In" and not customer:
                messages.warning(request,"Payment should be assigned to an Invoice and a Customer")
                return render(request,'add_payment.html',{'form':form,
                    'customers_list':Customers.objects.all(),
                    'producers_list':Producers.objects.all(),
                    'in_invoices':Invoices.objects.filter(cancelled=False,payment__isnull=True),
                    'out_invoices':IncomingInvoices.objects.filter(closed=False)})
        if payment_type == "Out" and not in_invoices and not producer:
                messages.warning(request,"Payment should be assigned to an Invoice and a Producer")
                return render(request,'add_payment.html',{'form':form,
                    'customers_list':Customers.objects.all(),
                    'producers_list':Producers.objects.all(),
                    'in_invoices':Invoices.objects.filter(cancelled=False,payment__isnull=True),
                    'out_invoices':IncomingInvoices.objects.filter(closed=False)})
        if payment_type == "Out" and not producer:
                messages.warning(request,"Payment should be assigned to an Invoice and a Producer")
                return render(request,'add_payment.html',{'form':form,
                    'customers_list':Customers.objects.all(),
                    'producers_list':Producers.objects.all(),
                    'in_invoices':Invoices.objects.filter(cancelled=False,payment__isnull=True),
                    'out_invoices':IncomingInvoices.objects.filter(closed=False)})
        if amount:
            if float(amount) < 0:
                messages.warning(request,"Payment amount cannot be less than Zero!")
                return render(request,'add_payment.html',{'form':form,
                    'customers_list':Customers.objects.all(),
                    'producers_list':Producers.objects.all(),
                    'in_invoices':Invoices.objects.filter(cancelled=False,payment__isnull=True),
                    'out_invoices':IncomingInvoices.objects.filter(closed=False)})
        if form.is_valid():

            if payment_type == "In":
                for invoice in out_invoices:
                    invoice_customer = Invoices.objects.get(pk=invoice).customer.name
                    selected_customer = Customers.objects.get(pk=customer).name
                    if selected_customer != invoice_customer:
                        messages.warning(request,"The selected Invoices do not belong to the same Customer")
                        return render(request,'add_payment.html',{'form':form,
                            'customers_list':Customers.objects.all(),
                            'producers_list':Producers.objects.all(),
                            'in_invoices':Invoices.objects.filter(cancelled=False,payment__isnull=True),
                            'out_invoices':IncomingInvoices.objects.filter(closed=False)})
                new_payment = Payments(
                    amount = amount,
                    payment_type = payment_type,
                    customer=Customers.objects.get(pk=customer),
                    date = date,
                    description = description
                )
                form = new_payment
                new_payment.save()
                for invoice in out_invoices:
                    out_invoice= Invoices.objects.get(pk=invoice)
                    out_invoice.payment = Payments.objects.get(pk=new_payment.pk)
                    out_invoice.closed = True
                    out_invoice.save()

            else:
                for invoice in out_invoices:
                    first_invoice_type = IncomingInvoices.objects.get(pk=in_invoices[0]).invoice_type
                    second_invoice_type = IncomingInvoices.objects.get(pk=invoice).invoice_type
                    if first_invoice_type != second_invoice_type:
                        messages.warning(request,"The selected Invoices do not the same type!")
                        return render(request,'add_payment.html',{'form':form,
                            'customers_list':Customers.objects.all(),
                            'producers_list':Producers.objects.all(),
                            'in_invoices':Invoices.objects.filter(cancelled=False,payment__isnull=True),
                            'out_invoices':IncomingInvoices.objects.filter(closed=False)})
                if IncomingInvoices.objects.get(pk=in_invoices[0]).producer:
                    for invoice in in_invoices:
                        invoice_producer = IncomingInvoices.objects.get(pk=invoice).producer.name
                        selected_producer = Producers.objects.get(pk=producer).name
                        if selected_producer != invoice_producer:
                            messages.warning(request,"The selected Invoices do not belong to the same Producer")
                            return render(request,'add_payment.html',{'form':form,
                                'customers_list':Customers.objects.all(),
                                'producers_list':Producers.objects.all(),
                                'in_invoices':Invoices.objects.filter(cancelled=False,payment__isnull=True),
                                'out_invoices':IncomingInvoices.objects.filter(closed=False)})
                new_payment = Payments(
                    amount = amount,
                    payment_type = payment_type,
                    producer=Producers.objects.get(pk=producer),
                    date = date,
                    description = description
                )
                form = new_payment
                new_payment.save()
                for invoice in in_invoices:
                    in_invoice= IncomingInvoices.objects.get(pk = invoice)
                    in_invoice.payment = Payments.objects.get(pk=new_payment.pk)
                    in_invoice.closed = True
                    in_invoice.save()
            messages.success(request,"Payment succesfully registered")
            return redirect('display_payments')
    else:
        form = PaymentForm()
        return render(request,'add_payment.html',{'form':form,
                    'customers_list':Customers.objects.all(),
                    'producers_list':Producers.objects.all(),
                    'in_invoices':Invoices.objects.filter(cancelled=False,payment__isnull=True),
                    'out_invoices':IncomingInvoices.objects.filter(closed=False)})
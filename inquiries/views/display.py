from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from inquiries.models import *
from inquiries.forms import *
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import csv
from inquiries.utils import render_to_pdf
from django.views.generic import View
from django.db.models import Sum, Avg
from django.utils import timezone
import datetime

year = datetime.datetime.now().year

def index(request):
    return render(request,'index.html')

@login_required
def display_customers(request):
    customers = Customers.objects.all()
    if "client"in request.GET:
        name = request.GET.get('client','')
        customers = Customers.objects.filter(name__icontains=name)
    context = {
        'customers': customers,
        'header': 'Current Customers',
    }
    return render (request, 'customers.html', context)
# @login_required
def display_orders(request):
    orders = Orders.objects.filter(date__icontains=datetime.datetime.now().year)
    context = {
        'orders': orders,
        'header': 'Running Orders',
    }
    if "year" or "client" or "search" in request.GET:
        year = request.GET.get('year',0)
        name = request.GET.get('client','')
        order = request.GET.get('search','')
        orders = Orders.objects.filter(Q(customer__name__icontains=name) &
                                       Q(order_due_date__icontains=year) &
                                       Q(order_number__icontains=order))
    context = {
        'orders': orders,
        'header': 'Running Orders',
    }
    return render (request, 'display_orders.html', context)
@login_required
def display_invoices(request):
    if "number" or "client" or "type" or "year" in request.GET:
        number = request.GET.get('number',0)
        sender = request.GET.get('client','')
        invoice_type = request.GET.get('type','')
        request_year = request.GET.get('year',year)
        invoices = Invoices.objects.filter(invoice_date__icontains=year)
        context= {
            'invoices':invoices,
        }
        if Invoices.objects.filter(Q(customer__name__icontains=sender)) and not Invoices.objects.filter(Q(producer__name__icontains=sender)):
            invoices = Invoices.objects.filter(Q(customer__name__icontains=sender) &
                                                Q(invoice_number__icontains=number) &
                                                Q(invoice_type__icontains=invoice_type)&
                                                Q(invoice_date__icontains=request_year))

        elif Invoices.objects.filter(Q(producer__name__icontains=sender)) and not Invoices.objects.filter(Q(customer__name__icontains=sender)):
            invoices = Invoices.objects.filter(Q(producer__name__icontains=sender) &
                                                Q(invoice_number__icontains=number) &
                                                Q(invoice_type__icontains=invoice_type)&
                                                Q(invoice_date__icontains=request_year))

        else:
            invoices = Invoices.objects.filter(Q(invoice_number__icontains=number) &
                                                Q(invoice_type__icontains=invoice_type)&
                                                Q(invoice_date__icontains=request_year))

        context = {
        'invoices': invoices,
        }
        return render(request,'invoices.html',context)
    else:
        return render(request,'invoices.html',context)
# @login_required
def incoming_invoices(request):
    if "number" or "producer" or "type" or "year" in request.GET:
        number = request.GET.get('number',0)
        sender = request.GET.get('producer','')
        invoice_type = request.GET.get('type','')
        request_year = request.GET.get('year',year)
        invoices = IncomingInvoices.objects.filter(invoice_date__icontains=year)
        context = {
                'invoices': invoices,
            }
        if IncomingInvoices.objects.filter(Q(customer__name__icontains=sender)) and not IncomingInvoices.objects.filter(Q(producer__name__icontains=sender)):
            invoices = IncomingInvoices.objects.filter(Q(customer__name__icontains=sender) &
                                                Q(invoice_number__icontains=number) &
                                                Q(invoice_type__icontains=invoice_type)&
                                                Q(invoice_date__icontains=request_year))

        elif IncomingInvoices.objects.filter(Q(producer__name__icontains=sender)) and not IncomingInvoices.objects.filter(Q(customer__name__icontains=sender)):
            invoices = IncomingInvoices.objects.filter(Q(producer__name__icontains=sender) &
                                                Q(invoice_number__icontains=number) &
                                                Q(invoice_type__icontains=invoice_type)&
                                                Q(invoice_date__icontains=request_year))

        else:
            invoices = IncomingInvoices.objects.filter(Q(invoice_number__icontains=number) &
                                                Q(invoice_type__icontains=invoice_type)&
                                                Q(invoice_date__icontains=request_year))
        context = {
                'invoices': invoices,
            }
        return render(request,'incoming_invoices.html',context)
    else:
        return render(request,'incoming_invoices.html',context)


@login_required
def select_customer(request):
    if "year" or "search" in request.GET:
        year = request.GET.get('year',0)
        order = request.GET.get('search','')
        customer_pk = request.GET.get('customer')
        customer = ''
        if customer_pk:
            customer = Customers.objects.get(pk=customer_pk).name
        calculations = Calculations.objects.filter(Q(production__load_date__icontains=year) &
                                                    Q(order__customer__name__icontains=customer) &
                                                    Q(production__order__order_number__icontains=order))
        context = {
        'calculations': calculations,
        'customers':Customers.objects.all()
        }
        return render(request,'select_customer.html',context)
    else:
        return render(request,'select_customer.html',context)
@login_required
def export_customer_csv(request):
    if "year" or "client" in request.GET:
        response = HttpResponse(content_type='text/csv')
        year = request.GET.get('year',0)
        name = request.GET.get('client','')
        calculations = Calculations.objects.filter(
            Q(production__load_date__icontains=year) &
            Q(order__customer__name__icontains=name)).values_list(
                'order__customer__name','order__order_number','sale_neto','sale_vat','sale_gross','amount_difference','days_late','profit','date','production__producer__name')
        writer = csv.writer(response)
        writer.writerow(['Customer','Order','Neto','Vat','Gross','Amount Difference','Days Late','Profit','Date','Producer'])
        for calculation in calculations:
            writer.writerow(calculation)
        response['Content-Disposition'] = 'attachment; filename="calculation-customer.csv"'
    return response
@login_required
def export_customer_pdf(request, *args, **kwargs):
    if "year" or "client" in request.GET:
        year = request.GET.get('year',0)
        name = request.GET.get('client','')
        sum_gross = 0
        sum_bonus = 0
        sum_neto = 0
        sum_profit = 0
        avg_days_late = 0
        sum_payments = 0
        s_payments = 0
        sum_vat = 0
        avg_amount_difference = 0
        debt = 0
        calculations = Calculations.objects.filter(production__load_date__icontains=year)
        if Productions.objects.filter(order__customer__name =name,load_date__icontains=year):
            calculations = Calculations.objects.filter(
                                                        Q(production__load_date__icontains=year) &
                                                        Q(order__customer__name__icontains=name))
            payments = Payments.objects.filter(customer__name__icontains=name,date__icontains=year)
            sum_payments_l = list(payments.aggregate(Sum('amount')).values())
            sum_payments = sum_payments_l[0]
            sum_neto_l = list(calculations.aggregate(Sum('sale_neto')).values())
            sum_neto = "{:.2f}".format(sum_neto_l[0])
            sum_vat_l = list(calculations.aggregate(Sum('sale_vat')).values())
            sum_vat = "{:.2f}".format(sum_vat_l[0])
            sum_gross_l = list(calculations.aggregate(Sum('sale_gross')).values())
            sum_gross = "{:.2f}".format(sum_gross_l[0])
            sum_profit_l = list(calculations.aggregate(Sum('profit')).values())
            sum_profit = "{:.2f}".format(sum_profit_l[0])
            avg_days_late_l = list(calculations.aggregate(Avg('days_late')).values())
            avg_days_late = "{:.1f}".format(avg_days_late_l[0])
            avg_amount_difference_l = list(calculations.aggregate(Avg('amount_difference')).values())
            avg_amount_difference = "{:.1f}".format(avg_amount_difference_l[0])
            debt = float(sum_neto)
            if sum_payments:
                s_payments = float(sum_payments)
            debt_l = float(sum_neto)-s_payments
            debt = round(debt_l,2)
        data = {
            'calculations': calculations,
            'year': year,
            'name': name,
            'sum_neto': sum_neto,
            'sum_vat': sum_vat,
            'sum_profit':sum_profit,
            'sum_gross': sum_gross,
            'avg_days_late': avg_days_late,
            'avg_amount_difference': avg_amount_difference,
            'sum_payments':sum_payments,
            'debt':debt,
        }
        pdf = render_to_pdf('pdf_customer.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

@login_required
def display_brands(request):
    brands = Brands.objects.order_by('customer')
    if "client" in request.GET:
        name = request.GET.get('client','')
        brands = Brands.objects.filter(customer__name__icontains=name)
    context = {
        'brands': brands,
        'header': 'Current Brands',
    }
    return render (request, 'brands.html', context)

@login_required
def display_production(request):
    production = Productions.objects.filter(production_due_date__icontains=datetime.datetime.now().year).order_by('production_due_date')
    if "year" or "client" or "search" in request.GET:
        year = request.GET.get('year',0)
        name = request.GET.get('client','')
        order = request.GET.get('search','')
        production = Productions.objects.filter(Q(order__customer__name__icontains=name) &
                                                Q(order__order_due_date__icontains=year) &
                                                Q(order__order_number__icontains=order))
    context = {
        'production': production,
        'header': 'Running Production',
    }
    return render (request, 'production.html', context)

# @login_required
def display_producers(request):
    producers = Producers.objects.all()
    if "client"in request.GET:
        name = request.GET.get('client','')
        producers = Producers.objects.filter(name__icontains=name)
    context = {
        'producers': producers,
        'header': 'Current Producers',
    }
    return render (request, 'producers.html', context)

@login_required
def select_producer(request):
    if "year"or "search" in request.GET:
        year = request.GET.get('year',0)
        order = request.GET.get('search','')
        producer_pk = request.GET.get('producer')
        producer = ''
        if producer_pk:
            producer = Producers.objects.get(pk=producer_pk).name
        calculations = Calculations.objects.filter(Q(production__producer__name__icontains=producer) &
                                                Q(production__load_date__icontains=year)&
                                                Q(production__order__order_number__icontains=order))
        context = {
                'calculations': calculations,
                'producers':Producers.objects.all()
                }
        return render(request,'select_producer.html',context)
    else:
        return render(request,'select_producer.html',context)
@login_required
def export_producer_csv(request):
    if "year" or "producer" in request.GET:
        year = request.GET.get('year',0)
        name = request.GET.get('producer','')
        response = HttpResponse(content_type='text/csv')
        calculations = Calculations.objects.filter(
            Q(production__producer__name__icontains=name) &
            Q(production__load_date__icontains=year)).values_list(
                'production__producer__name','order__order_number','buy_gross','buy_bonus','buy_neto','amount_difference','days_late','profit','date','order__customer__name')
        writer = csv.writer(response)
        writer.writerow(['Producer','Order','Gross','Bonus','Neto','Amount Difference','Days Late','Profit','Date','Customer'])
        for calculation in calculations:
            writer.writerow(calculation)

        response['Content-Disposition'] = 'attachment; filename="calculation-producer.csv"'
    return response
@login_required
def export_producer_pdf(request, *args, **kwargs):
    if "year" or "producer" in request.GET:
        year = request.GET.get('year',0)
        name = request.GET.get('producer','')
        sum_diverses = 0
        sum_gross = 0
        sum_bonus = 0
        sum_neto = 0
        sum_profit = 0
        avg_days_late = 0
        sum_reklamations = 0
        sum_payments = 0
        s_diverses = 0
        s_reklamations = 0
        s_payments = 0
        avg_amount_difference = 0
        debt = 0
        calculations = Calculations.objects.filter(production__load_date__icontains = year)
        if Productions.objects.filter(producer__name =name,load_date__icontains=year):
            calculations = Calculations.objects.filter(
                Q(production__producer__name__icontains=name) &
                Q(production__load_date__icontains=year))
            payments = Payments.objects.filter(producer__name__icontains=name,date__icontains=year)
            reklamations = Items.objects.filter(Q(producer__name__icontains=name) & Q(invoice__invoice_date__icontains=year) & Q(invoice__invoice_type__icontains="Reklamation"))
            diverses = Items.objects.filter(Q(producer__name__icontains=name) & Q(invoice__invoice_date__icontains=year) & Q(invoice__invoice_type__icontains="Diverse"))
            sum_diverses_l = list(diverses.aggregate(Sum('amount')).values())
            sum_diverses = sum_diverses_l[0]
            sum_reklamations_l = list(reklamations.aggregate(Sum('amount')).values())
            sum_reklamations = sum_reklamations_l[0]
            sum_payments_l = list(payments.aggregate(Sum('amount')).values())
            sum_payments = sum_payments_l[0]
            sum_gross_l = list(calculations.aggregate(Sum('buy_gross')).values())
            sum_gross = "{:.2f}".format(sum_gross_l[0])
            sum_bonus_l = list(calculations.aggregate(Sum('buy_bonus')).values())
            sum_bonus = "{:.2f}".format(sum_bonus_l[0])
            sum_neto_l = list(calculations.aggregate(Sum('buy_neto')).values())
            sum_neto = "{:.2f}".format(sum_neto_l[0])
            sum_profit_l = list(calculations.aggregate(Sum('profit')).values())
            sum_profit = "{:.2f}".format(sum_profit_l[0])
            avg_days_late_l = list(calculations.aggregate(Avg('days_late')).values())
            avg_days_late = "{:.1f}".format(avg_days_late_l[0])
            avg_amount_difference_l = list(calculations.aggregate(Avg('amount_difference')).values())
            avg_amount_difference = "{:.1f}".format(avg_amount_difference_l[0])
            debt = float(sum_neto)
            if sum_payments:
                s_payments = float(sum_payments)
            if sum_reklamations:
                s_reklamations-float(sum_reklamations)
            if sum_diverses:
                s_diverses-float(sum_diverses)
            debt_l = float(sum_neto)-s_diverses-s_payments-s_reklamations
            debt = round(debt_l,2)
        data = {
            'calculations': calculations,
            'year': year,
            'name': name,
            'sum_gross': sum_gross,
            'sum_bonus': sum_bonus,
            'sum_neto': sum_neto,
            'sum_profit': sum_profit,
            'sum_reklamations':sum_reklamations,
            'sum_diverses':sum_diverses,
            'avg_days_late': avg_days_late,
            'avg_amount_difference': avg_amount_difference,
            'sum_payments':sum_payments,
            'debt':debt,
        }
        pdf = render_to_pdf('pdf_producer.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


@login_required
def display_payments(request):
    payments = Payments.objects.all()
    if "year" or "type" or "client" in request.GET:
        request_year = request.GET.get('year',year)
        sender = request.GET.get('client','')
        payment_type = request.GET.get('type','')
        payments = Payments.objects.filter(Q(date__icontains=year))
        context = {
        'payments' : payments
        }
        if Payments.objects.filter(Q(customer__name__icontains=sender)) and not Payments.objects.filter(Q(producer__name__icontains=sender)):
            payments = Payments.objects.filter(Q(customer__name__icontains=sender) &
                                                Q(payment_type__icontains=payment_type)&
                                                Q(date__icontains=request_year))

        elif Payments.objects.filter(Q(producer__name__icontains=sender)) and not Payments.objects.filter(Q(customer__name__icontains=sender)):
            payments = Payments.objects.filter(Q(producer__name__icontains=sender) &
                                                Q(payment_type__icontains=payment_type)&
                                                Q(date__icontains=request_year))

        else:
            payments = Payments.objects.filter(Q(payment_type__icontains=payment_type)&
                                                Q(date__icontains=request_year))

    context = {
        'payments' : payments
    }
    return render(request,'payments.html',context)

@login_required
def accounting(request):
    context = {
    }
    return render(request,'accounting.html',context)
@login_required
def order_lookup(request):
    search = Productions.objects.all()
    search = ''
    context = {
        'search': search,
    }
    if "order_search" in request.GET:
        value = request.GET['order_search']
        search = Productions.objects.filter(
            Q(order__order_number__iexact=value)
        )
        context = {
        'search': search,
        }
        return render(request,'order_lookup.html',context)
    else:
        return render(request,'order_lookup.html',context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from inquiries.models import *
from inquiries.functions import create_calculation, edit_calculation
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Sum, Avg
from inquiries.utils import render_to_pdf
from django.http import HttpResponse

@login_required
def invoice_detail(request,pk):
    invoices = Items.objects.filter(invoice=pk)
    netto_l = list(invoices.aggregate(Sum('total')).values())
    netto = "{:.2f}".format(netto_l[0])
    vat_l = list(invoices.aggregate(Sum('vat')).values())
    vat = "{:.2f}".format(vat_l[0])
    gross_l = list(invoices.aggregate(Sum('total_sum')).values())
    gross = "{:.2f}".format(gross_l[0])
    date = Invoices.objects.get(pk=pk).invoice_date
    number = Invoices.objects.get(pk=pk).invoice_number
    status = Invoices.objects.get(pk=pk).cancelled
    closed = Invoices.objects.get(pk=pk).closed
    invoice_status = ''
    if Invoices.objects.get(pk=pk).invoice_type == 'Reklamation':
        name = invoices[0].producer.full_name
        address = invoices[0].producer.address
        city = invoices[0].producer.city
        country = invoices[0].producer.country
    else:
        name = invoices[0].customer.full_name
        address = invoices[0].customer.address
        city = invoices[0].customer.city
        country = invoices[0].customer.country
    if status:
        invoice_status = 'Cancelled'
    return render(request,'invoice_detail.html',
                 {'pk':pk,'invoices':invoices,'netto':netto,
                 'vat':vat,'gross':gross,'name':name,'number':number,'date':date,
                 'address':address,'city':city,'country':country,'status':status,'invoice_status':invoice_status,'closed':closed})

def export_invoice_pdf(request,pk):
    invoices = Items.objects.filter(invoice=pk)
    netto_l = list(invoices.aggregate(Sum('total')).values())
    netto = "{:.2f}".format(netto_l[0])
    vat_l = list(invoices.aggregate(Sum('vat')).values())
    vat = "{:.2f}".format(vat_l[0])
    gross_l = list(invoices.aggregate(Sum('total_sum')).values())
    gross = "{:.2f}".format(gross_l[0])
    date = Invoices.objects.get(pk=pk).invoice_date
    number = Invoices.objects.get(pk=pk).invoice_number
    if Invoices.objects.get(pk=pk).invoice_type == 'Reklamation':
        name = invoices[0].producer.full_name
        address = invoices[0].producer.address
        city = invoices[0].producer.city
        country = invoices[0].producer.country
    else:
        name = invoices[0].customer.full_name
        address = invoices[0].customer.address
        city = invoices[0].customer.city
        country = invoices[0].customer.country

    pdf = render_to_pdf('pdf_invoice.html', {'invoices':invoices,'netto':netto,
                 'vat':vat,'gross':gross,'name':name,'number':number,'date':date,
                 'address':address,'city':city,'country':country})
    return HttpResponse(pdf, content_type='application/pdf')
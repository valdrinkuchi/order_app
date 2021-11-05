from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from inquiries.models import *
from inquiries.forms import *
from django.contrib.auth.decorators import login_required

@login_required
def confirm_delete(request,pk,model,template,context):

    if request.method =="POST":
        if (context == 'Production'):
            order_object = model.objects.get(pk=pk).order
            order_object.in_production = False
            order_object.save()
        if (context == 'InInvoices'):
            production_obj = Productions.objects.filter(in_invoice=pk)
            documents_obj = Documents.objects.filter(invoice=pk)
            for file in documents_obj:
                file_obj = Documents.objects.get(document=file)
                file_obj.delete()
            if production_obj:
                for production in production_obj:
                    production.assigned_in_invoice = False
                    production.save()
        if (context == 'Payment'):
            invoices = Invoices.objects.filter(payment=pk)
            for invoice in invoices:
                invoice.closed = False
                invoice.save()

        model.objects.filter(pk=pk).delete()
        messages.success(request,"The Instance has been Deleted!")
        return redirect(template)

    info = get_object_or_404(model, pk=pk)
    context = {
        'Model': info,
        'template': template,
    }
    return render(request,'confirm_delete.html', context)

def delete_orders(request,pk):
    return confirm_delete(request,pk,Orders,'display_orders','Order')

def delete_customers(request,pk):
    return confirm_delete(request,pk, Customers,'display_customers','Customer')

def delete_producer(request,pk):
    return confirm_delete(request,pk, Producers,'display_producers','Producer')

def delete_brands(request,pk):
    return confirm_delete(request,pk, Brands,'display_brands','Brand')

def delete_production(request,pk):
    return confirm_delete(request,pk, Productions,'display_production','Production')

def delete_payment(request,pk):
    return confirm_delete(request,pk, Payments,'display_payments','Payment')

def delete_in_invoice(request,pk):
    return confirm_delete(request,pk, IncomingInvoices,'incoming_invoices','InInvoices')








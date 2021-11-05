from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from inquiries.models import *
from inquiries.forms import *
from inquiries.functions import create_calculation, edit_calculation
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q

@login_required
def edit_payment(request,pk):
    info = get_object_or_404(Payments, pk=pk)
    customer = info.customer
    producer = info.producer
    if request.method =='POST':
        form = PaymentForm(request.POST, instance=info)
        payment_type = request.POST.get('payment_type')
        amount = request.POST.get('amount')
        date = datetime.strptime(form['date'].data, '%Y-%m-%d').date()
        in_invoices = request.POST.getlist('in_invoices[]')
        out_invoices = request.POST.getlist('out_invoices[]')
        description = request.POST.get('description')
        if info.customer:
            customer = info.customer
        if info.producer:
            producer = info.producer
        if amount:
            if float(amount) < 0:
                messages.warning(request,"The amount cannot be negative!")
                return render(request,'edit_payment.html',{'form': form,'info':info,
                            'in_sel_invoices':Invoices.objects.filter(payment=pk),
                            'out_sel_invoices':IncomingInvoices.objects.filter(payment=pk),
                            'in_invoices':Invoices.objects.filter(payment__isnull=True),
                            'out_invoices':IncomingInvoices.objects.filter(Q(payment__isnull=True))})
        if form.is_valid():
            if payment_type == "In":
                payment_obj = Payments.objects.get(pk = pk)
                payment_obj.amount = amount
                payment_obj.payment_type = payment_type
                payment_obj.date = date
                payment_obj.description = description
                payment_obj.save()
                for invoice in out_invoices:
                    out_invoice= Invoices.objects.get(pk=invoice)
                    out_invoice.payment = Payments.objects.get(pk=payment_obj.pk)
                    out_invoice.closed = True
                    out_invoice.save()

            else:
                payment_obj = Payments.objects.get(pk = pk)
                payment_obj.amount = amount
                payment_obj.payment_type = payment_type
                payment_obj.date = date
                payment_obj.description = description
                payment_obj.save()
                for invoice in in_invoices:
                    in_invoice = IncomingInvoices.objects.get(pk=invoice)
                    in_invoice.payment = Payments.objects.get(pk=payment_obj.pk)
                    in_invoice.closed = True
                    in_invoice.save()
            messages.success(request,"Payment succesfully edited")
            return redirect('display_payments')
    else:
        form = PaymentForm(instance=info)
        return render(request,'edit_payment.html',{'form': form,'info':info,
                            'in_sel_invoices':Invoices.objects.filter(payment=pk),
                            'out_sel_invoices':IncomingInvoices.objects.filter(payment=pk),
                            'in_invoices':Invoices.objects.filter(payment__isnull=True,customer=customer,producer=producer),
                            'out_invoices':IncomingInvoices.objects.filter(payment__isnull=True,customer=customer,producer=producer)})
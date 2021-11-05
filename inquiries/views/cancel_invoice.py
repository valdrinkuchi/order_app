from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from inquiries.models import *
from inquiries.forms import *
from django.contrib.auth.decorators import login_required

@login_required
def cancel_invoice(request,pk):

    if request.method =="POST":
        invoice = Invoices.objects.get(pk=pk)
        invoice.cancelled = True
        invoice.save()
        productions = Productions.objects.filter(invoice=pk)
        for production in productions:
            production.active = True
            production.save()
        messages.success(request,"The Instance has been Cancelled!")
        return redirect('display_invoices')

    info = get_object_or_404(Invoices, pk=pk)
    context = {
        'Model': info,
    }
    return render(request,'confirm_cancelling.html', context)
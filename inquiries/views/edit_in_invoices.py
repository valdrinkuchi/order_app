from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from inquiries.models import *
from inquiries.forms import *
from inquiries.functions import create_calculation, edit_calculation
from django.contrib.auth.decorators import login_required
from datetime import datetime


@login_required
def edit_in_invoice(request,pk):
    info = get_object_or_404(IncomingInvoices, pk=pk)
    documents = Documents.objects.filter(invoice=pk)
    production_list = Productions.objects.filter(in_invoice=pk)
    if request.method =='POST':
        form = IncomingInvoiceEditForm(request.POST, instance=info)

        if form.is_valid():

            messages.success(request, "Invoice succesfully edited")
            return redirect('incoming_invoices')
    else:
        form = IncomingInvoiceEditForm(instance=info)
        selected_invoice_type = info.invoice_type
        return render(request, 'edit_in_invoices.html', {'form': form,'Model': info,'documents':documents,'production_list':production_list,'selected_invoice_type':selected_invoice_type})
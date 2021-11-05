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
def register_invoice(request):
    form = IncomingInvoiceForm(request.POST or None)
    if request.method =='POST':
        form = IncomingInvoiceForm(request.POST)
        in_production_list = request.POST.getlist('productions[]')
        invoice_type = form['invoice_type'].data
        customer = request.POST.get('customer')
        producer = request.POST.get('producer')
        number = request.POST.get('invoice_number')
        documents = request.FILES.getlist('documents')
        description = request.POST.get('description')
        date = datetime.strptime(form['invoice_date'].data, '%Y-%m-%d').date()
        if invoice_type =='Reklamation' and not customer:
                messages.warning(request, "Customer field cannot be empty!")
                return render(request,'register_invoice.html',{'form':form,
                    'production_list': Productions.objects.filter(assigned_in_invoice=False),
                    'producers_list':Producers.objects.all(),
                    'customers_list':Customers.objects.all()})
        if invoice_type =='Diverse' and not producer and not customer:
            messages.warning(request, "The 'Diverse' Invoice must be assigned to a customer or a producer!")
            return render(request,'register_invoice.html',{'form':form,
                'production_list': Productions.objects.filter(assigned_in_invoice=False),
                'producers_list':Producers.objects.all(),
                'customers_list':Customers.objects.all()})
        if invoice_type == 'Invoice' and not documents:
                messages.warning(request, "Invoice must contain files to be uploaded!")
                return render(request,'register_invoice.html',{'form':form,
                    'production_list': Productions.objects.filter(assigned_in_invoice=False),
                    'producers_list':Producers.objects.all(),
                    'customers_list':Customers.objects.all()})
        if invoice_type == 'Invoice' and producer:
            sel_producer = Producers.objects.get(pk=producer).name
            for prod in in_production_list:
                inv_producer = Productions.objects.get(pk=prod).producer.name
                if sel_producer != inv_producer:
                    messages.warning(request, "Selected orders must belong to the same producer!")
                    return render(request,'register_invoice.html',{'form':form,
                        'production_list': Productions.objects.filter(assigned_in_invoice=False),
                        'producers_list':Producers.objects.all(),
                        'customers_list':Customers.objects.all()})
        if documents:
            if len(documents)>3:
                messages.warning(request, "Cannot upload more than three files!")
                return render(request,'register_invoice.html',{'form':form,
                    'production_list': Productions.objects.filter(assigned_in_invoice=False),
                    'producers_list':Producers.objects.all(),
                    'customers_list':Customers.objects.all()})
            for file in documents:
                filesize= file.size
                if filesize > 1048576:
                    messages.warning(request, "The file size is too big!")
                    return render(request,'register_invoice.html',{'form':form,
                        'production_list': Productions.objects.filter(assigned_in_invoice=False),
                        'producers_list':Producers.objects.all(),
                        'customers_list':Customers.objects.all()})

        if form.is_valid():
            if invoice_type =='Invoice':
                new_invoice = IncomingInvoices(
                                invoice_number=number,
                                invoice_type=invoice_type,
                                invoice_date=date,
                                producer = Producers.objects.get(pk=producer),
                                )

                form = new_invoice
                new_invoice.save()
                for production in in_production_list:
                    production_obj = Productions.objects.get(pk=production)
                    production_obj.in_invoice = IncomingInvoices.objects.get(pk=new_invoice.pk)
                    production_obj.assigned_in_invoice = True
                    production_obj.save()

                for file in documents:
                    new_documents = Documents(
                        invoice = IncomingInvoices.objects.get(pk=new_invoice.pk),
                        document = file,
                        description = description
                    )
                    form = new_documents
                    new_documents.save()

            if invoice_type =='Reklamation' and customer:
                new_invoice = IncomingInvoices(
                                invoice_number=number,
                                invoice_type=invoice_type,
                                invoice_date=date,
                                customer = Customers.objects.get(pk=customer)
                )

                form = new_invoice
                new_invoice.save()
                for file in documents:
                    invoice = IncomingInvoices.objects.get(invoice_number=number).pk
                    new_documents = Documents(
                        invoice = IncomingInvoices.objects.get(pk=invoice),
                        document = file,
                        description = description
                    )
                    form = new_documents
                    new_documents.save()

            if invoice_type =='Diverse' and customer:
                new_invoice = IncomingInvoices(
                                invoice_number=number,
                                invoice_type=invoice_type,
                                invoice_date=date,
                                customer = Customers.objects.get(pk=customer),
                                )

                form = new_invoice
                new_invoice.save()
                for file in documents:
                    invoice = IncomingInvoices.objects.get(invoice_number=number).pk
                    new_documents = Documents(
                        invoice = IncomingInvoices.objects.get(pk=invoice),
                        document = file,
                        description = description
                    )
                    form = new_documents
                    new_documents.save()

            if invoice_type =='Diverse' and producer:
                new_invoice = IncomingInvoices(
                                invoice_number=number,
                                invoice_type=invoice_type,
                                invoice_date=date,
                                producer = Producers.objects.get(pk=producer),
                                )

                form = new_invoice
                new_invoice.save()
                for file in documents:
                    invoice = IncomingInvoices.objects.get(invoice_number=number).pk
                    new_documents = Documents(
                        invoice = IncomingInvoices.objects.get(pk=invoice),
                        document = file,
                        description = description
                    )
                    form = new_documents
                    new_documents.save()
                messages.success(request, 'Invoice' + " succesfully registered")
                return redirect('incoming_invoices')
        form.save()
        messages.success(request, 'Invoice' + " succesfully registered")
        return redirect('incoming_invoices')
    else:
        form = IncomingInvoiceForm()
        return render(request,'register_invoice.html',{'form':form,
        'production_list': Productions.objects.filter(assigned_in_invoice=False),
        'producers_list':Producers.objects.all(),
        'customers_list':Customers.objects.all()})
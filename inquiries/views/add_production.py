from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from inquiries.models import *
from inquiries.forms import *
from inquiries.views.edit import edit_info
from inquiries.functions import create_calculation,add_calculation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
def is_form_valid(request, form):
    is_valid = True

    if isinstance(form,RawProductionForm):
        new_order_number = form['order'].data
        price = float(form['production_price'].data)
        confirmed_date = datetime.strptime(form['production_due_date'].data, '%Y-%m-%d').date()
        order_signed_date = Orders.objects.get(pk=new_order_number).date
        load_count = form['production_load_count'].data
        load_date = form['load_date'].data
        if (not load_count and load_date) or (not load_date and load_count):
            is_valid = False
            messages.warning(request,"Amount,Load Date or Invoice Number Error. Please check these fields!")
        if price < 0:
            is_valid = False
            messages.warning(request, "Price cannot be negative!")
        elif order_signed_date >= confirmed_date:
            is_valid = False
            messages.warning(request, "Delivery date can not be earlier than signed date!")

        if load_date:
            load_date = datetime.strptime(form['load_date'].data, '%Y-%m-%d').date()
            if order_signed_date >= load_date:
                is_valid = False
                messages.warning(request, "Loading date can not be earlier than signed date!")
        # if invoice:
        #     if IncomingInvoices.objects.get(pk=invoice):
        #         invoice_producer = IncomingInvoices.objects.get(pk=invoice).producer
        #         order_producer = Orders.objects.get(pk=new_order_number).producer
        #         if invoice_producer != order_producer:
        #             is_valid = False
        #             messages.warning(request, "This Order doesn't belond to this Producer!")
    return is_valid


@login_required
def add_production(request):
    form = RawProductionForm()
    if  request.method =='POST':
        form = RawProductionForm(request.POST)
        if not is_form_valid(request, form):
            return render(request,'add_production.html',{'form':form})
        if form.is_valid():
            order_id = form['order'].data
            price = float(form['production_price'].data)
            bonus = float(form['bonus'].data)
            due_date = datetime.strptime(form['production_due_date'].data, '%Y-%m-%d').date()
            load_date = form['load_date'].data
            amount = form['production_load_count'].data
            producer = request.POST.get('producer')
            if load_date and amount:
                load_date = datetime.strptime(form['load_date'].data, '%Y-%m-%d').date()
                amount = int(form['production_load_count'].data)
                new_object = Productions( order = Orders.objects.get(pk=order_id),
                                            production_due_date=due_date,
                                            load_date=load_date,
                                            production_load_count=amount,
                                            production_price=price,
                                            bonus=bonus,
                                            producer=Producers.objects.get(pk=producer))
                form = new_object
                new_object.save()
                order_obj = Orders.objects.get(pk=order_id)
                order_obj.in_production = False
                order_obj.save()
                if amount >0 and load_date:
                    order_obj = Orders.objects.get(pk=order_id)
                    order_obj.in_production = False
                    order_obj.save()
                    new_calculation = add_calculation(form,order_id)
                    new_calculation.production = form
                    new_calculation.save()
                    new_object.save()
                messages.success(request, 'Production' + " succesfully created")
                return redirect('display_production')
            else:
                new_object = Productions(
                                        order = Orders.objects.get(pk=order_id),
                                        production_due_date=due_date,
                                        production_price=price,
                                        bonus=bonus,
                                        producer=Producers.objects.get(pk=producer))

                new_object.save()
                order_obj = Orders.objects.get(pk=order_id)
                order_obj.in_production = True
                order_obj.save()
            messages.success(request, 'Production' + " succesfully created")
            return redirect('display_production')
    else:
        form = RawProductionForm()
        return render(request,'add_production.html',{'form':form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from inquiries.models import *
from inquiries.forms import *
from inquiries.functions import create_calculation, edit_calculation
from django.contrib.auth.decorators import login_required
from datetime import datetime

def is_edit_valid(request,form):
    is_valid = True

    if isinstance(form,ProductionForm):
        new_order_number = form['order'].data
        order_signed_date = Orders.objects.get(pk=new_order_number).date
        confirmed_date = datetime.strptime(form['production_due_date'].data, '%Y-%m-%d').date()
        load_count = form['production_load_count'].data
        load_date = form['load_date'].data
        if load_count == '0':
            is_valid = False
            messages.warning(request, "Amount cannot be Zero!")
        price = float(form['production_price'].data)

        if price < 0:
            is_valid = False
            messages.warning(request, "Price cannot be negative!")

        if (not load_count and load_date) or (not load_date and load_count):
            is_valid = False
            messages.warning(request,"Amount,Load Date or Invoice Number Error. Please check these fields!")
        if (not load_count and not load_date):
            is_valid = True

        if order_signed_date >= confirmed_date:
            is_valid = False
            messages.warning(request, "Delivery date can not be earlier than signed date!")

        if load_date:
            load_date = datetime.strptime(form['load_date'].data, '%Y-%m-%d').date()
            if order_signed_date >= load_date:
                is_valid = False
                messages.warning(request, "Loading date can not be earlier than signed date!")


    return is_valid

@login_required
def edit_production(request,pk):
    info = get_object_or_404(Productions, pk=pk)
    if request.method =='POST':
        form = ProductionForm(request.POST, instance=info)
        if not is_edit_valid(request, form):
            return render(request,'edit_production.html',{'form': form,'Model': info,})
        if form.is_valid():
            obj = form
            order_id = form['order'].data
            load_date = form['load_date'].data
            amount = form['production_load_count'].data
            calculation_test = Calculations.objects.filter(order=order_id)
            if calculation_test:
                obj.save()
                create_calculation(form).save()
                messages.success(request, 'Production' + " succesfully edited")
                return redirect('display_production')
            elif amount and load_date:
                order_obj = Orders.objects.get(pk=order_id)
                order_obj.in_production = False
                order_obj.save()
                new_calculation = create_calculation(form, True)
                obj.save()
                new_calculation.productions = obj
                new_calculation.save()
                messages.success(request, 'Production' + " succesfully edited")
                return redirect('display_production')
        messages.success(request, "Production succesfully edited")
        return redirect('display_production')
    else:
        form = ProductionForm(instance=info)
        return render(request, 'edit_production.html', {'form': form,'Model': info,})
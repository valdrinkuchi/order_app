from inquiries.models import *
from inquiries.forms import *
from inquiries.views import *
import datetime
vat = 0.19

def add_calculation(form,order_id):
    order_id = form.order_id
    order_number = Orders.objects.get(pk=order_id).order_number
    loaded_amount = form.production_load_count
    ordered_amount = Orders.objects.get(order_number=order_number).order_pcs
    order_price = Orders.objects.get(order_number=order_number).price
    production_price = float(form.production_price)
    confirmed_date = form.production_due_date
    load_date = form.load_date
    discount = (form.bonus)/100
    client_discount = Orders.objects.get(pk=order_id).customer.bonus/100

    sale_neto_sum = (loaded_amount*order_price)-(loaded_amount*order_price*client_discount)
    out_neto_sum = round(sale_neto_sum,2)
    sale_sum_vat = (sale_neto_sum*vat)
    out_sum_vat = round(sale_sum_vat,2)
    sale_gross_sum = (out_neto_sum + out_sum_vat)
    out_gross_sum = round(sale_gross_sum,2)

    float_difference = loaded_amount-ordered_amount
    difference = int(float_difference)
    late_delivery = load_date-confirmed_date

    buy_neto_sum = (loaded_amount*production_price)-(loaded_amount*production_price*discount)
    in_neto_sum = round(buy_neto_sum,2)
    buy_bonus = (loaded_amount*production_price*discount)
    in_buy_bonus = round(buy_bonus,2)
    buy_gross_sum = (loaded_amount*production_price)
    in_buy_gross_sum = round(buy_gross_sum,2)

    profit = round((out_neto_sum-in_neto_sum),2)
    new_instance = Calculations(days_late=late_delivery.days,
                                amount_difference=difference,
                                sale_neto=out_neto_sum,
                                sale_vat=out_sum_vat,
                                sale_gross=out_gross_sum,
                                buy_neto=in_neto_sum,
                                buy_bonus=in_buy_bonus,
                                buy_gross=in_buy_gross_sum,
                                profit=profit,
                                order = Orders.objects.get(pk=order_id),
                                production = Productions.objects.get(order=order_id),
                                date = Productions.objects.get(order=order_id).load_date,
                                )
    return new_instance


def edit_calculation(form):
    order_number = form['order_number'].data
    order_id = Orders.objects.get(order_number=order_number).pk
    loaded_amount = Productions.objects.get(order=order_id).production_load_count
    str_ordered_amount = form['order_pcs'].data
    ordered_amount = int(str_ordered_amount)
    str_order_price = form['price'].data
    order_price = float(str_order_price)
    production_price = Productions.objects.get(order=order_id).production_price
    confirmed_date = Productions.objects.get(order=order_id).production_due_date
    load_date = Productions.objects.get(order=order_id).load_date
    discount = Productions.objects.get(order=order_id).bonus/100
    client_discount = Orders.objects.get(pk=order_id).customer.bonus/100

    sale_neto_sum = (loaded_amount*order_price)-(loaded_amount*order_price*client_discount)
    out_neto_sum = round(sale_neto_sum,2)
    sale_sum_vat = (sale_neto_sum*vat)
    out_sum_vat = round(sale_sum_vat,2)
    sale_gross_sum = (out_neto_sum + out_sum_vat)
    out_gross_sum = round(sale_gross_sum,2)

    float_difference = loaded_amount-ordered_amount
    difference = int(float_difference)
    late_delivery = load_date-confirmed_date

    buy_neto_sum = (loaded_amount*production_price)-(loaded_amount*production_price*discount)
    in_neto_sum = round(buy_neto_sum,2)
    buy_bonus = (loaded_amount*production_price*discount)
    in_buy_bonus = round(buy_bonus,2)
    buy_gross_sum = (loaded_amount*production_price)
    in_buy_gross_sum = round(buy_gross_sum,2)

    profit = round((out_neto_sum-in_neto_sum),2)

    already_existing_calculation = Calculations.objects.get(order=order_id)
    already_existing_calculation.days_late = late_delivery.days
    already_existing_calculation.amount_difference = difference
    already_existing_calculation.sale_neto = out_neto_sum
    already_existing_calculation.sale_vat = out_sum_vat
    already_existing_calculation.sale_gross = out_gross_sum
    already_existing_calculation.buy_neto = in_neto_sum
    already_existing_calculation.buy_bonus = in_buy_bonus
    already_existing_calculation.buy_gross = in_buy_gross_sum
    already_existing_calculation.profit = profit
    already_existing_calculation.date = Productions.objects.get(order=order_id).load_date
    return already_existing_calculation

def create_calculation(form, create_new = False):
    order_id = form['order'].data
    order_number = Orders.objects.get(pk=order_id).order_number
    str_loaded_amount = form['production_load_count'].data
    if str_loaded_amount:
        loaded_amount = int(str_loaded_amount)
    ordered_amount = Orders.objects.get(order_number=order_number).order_pcs
    order_price = Orders.objects.get(order_number=order_number).price
    production_price = float(form['production_price'].data)
    confirmed_date = datetime.datetime.strptime(form['production_due_date'].data, '%Y-%m-%d').date()
    load_date = datetime.datetime.strptime(form['load_date'].data, '%Y-%m-%d').date()
    discount = float(form['bonus'].data)/100
    client_discount = Orders.objects.get(pk=order_id).customer.bonus/100

    sale_neto_sum = (loaded_amount*order_price)-(loaded_amount*order_price*client_discount)
    out_neto_sum = round(sale_neto_sum,2)
    sale_sum_vat = (sale_neto_sum*vat)
    out_sum_vat = round(sale_sum_vat,2)
    sale_gross_sum = (out_neto_sum + out_sum_vat)
    out_gross_sum = round(sale_gross_sum,2)

    float_difference = loaded_amount-ordered_amount
    difference = int(float_difference)
    late_delivery = load_date-confirmed_date

    buy_neto_sum = (loaded_amount*production_price)-(loaded_amount*production_price*discount)
    in_neto_sum = round(buy_neto_sum,2)
    buy_bonus = (loaded_amount*production_price*discount)
    in_buy_bonus = round(buy_bonus,2)
    buy_gross_sum = (loaded_amount*production_price)
    in_buy_gross_sum = round(buy_gross_sum,2)

    profit = round((out_neto_sum-in_neto_sum),2)
    if create_new:
        new_instance = Calculations(days_late=late_delivery.days,
                                    amount_difference=difference,
                                    sale_neto=out_neto_sum,
                                    sale_vat=out_sum_vat,
                                    sale_gross=out_gross_sum,
                                    buy_neto=in_neto_sum,
                                    buy_bonus=in_buy_bonus,
                                    buy_gross=in_buy_gross_sum,
                                    profit=profit,
                                    order = Orders.objects.get(pk=order_id),
                                    production = Productions.objects.get(order=order_id),
                                    date = Productions.objects.get(order=order_id).load_date,
                                    )
        return new_instance
    else:
        already_existing_calculation = Calculations.objects.get(order=order_id)
        already_existing_calculation.days_late = late_delivery.days
        already_existing_calculation.amount_difference = difference
        already_existing_calculation.sale_neto = out_neto_sum
        already_existing_calculation.sale_vat = out_sum_vat
        already_existing_calculation.sale_gross = out_gross_sum
        already_existing_calculation.buy_neto = in_neto_sum
        already_existing_calculation.buy_bonus = in_buy_bonus
        already_existing_calculation.buy_gross = in_buy_gross_sum
        already_existing_calculation.profit = profit
        already_existing_calculation.date = Productions.objects.get(order=order_id).load_date
        return already_existing_calculation





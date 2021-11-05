from django import forms
from .models import *
from django.forms.widgets import HiddenInput
from inquiries.views import *
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.http import HttpResponseRedirect


class DateInput(forms.DateInput):
    input_type = 'date'

class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ('order_number','article','date','order_due_date','order_pcs','customer','price','brand','description')
        widgets = {'date':DateInput(),'order_due_date':DateInput()}
    def __init__(self, *args, **kwargs):
        super(OrdersForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('customer_number','name','full_name','address','city','delivery_address','delivery_address_2','postal_code','country','bonus')
    def __init__(self, *args, **kwargs):
        super(CustomersForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producers
        fields = ('producer_number','name','full_name','address','city','country')
    def __init__(self, *args, **kwargs):
        super(ProducerForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
class BrandsForm(forms.ModelForm):
    class Meta:
        model = Brands
        fields = ('brand_name','customer')
    def __init__(self, *args, **kwargs):
        super(BrandsForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
class ProductionForm(forms.ModelForm):
    class Meta:
        model = Productions
        fields = ('order','production_due_date','load_date','production_load_count','production_price','producer','bonus')
        widgets = {'order':HiddenInput(),'production_due_date':DateInput(),'load_date':DateInput()}
    def __init__(self,*args,**kwargs):
        super(ProductionForm,self).__init__(*args,**kwargs)
        self.fields['order'].label = ""
        self.fields['production_load_count'].required = False
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })


class RawProductionForm(forms.Form):
    order = forms.ModelChoiceField(queryset=Orders.objects.filter(productions__isnull=True))
    producer = forms.ModelChoiceField(queryset=Producers.objects.all())
    production_due_date = forms.DateField(label="Due Date",widget=DateInput())
    load_date = forms.DateField(required=False, label="Load Date",widget=DateInput())
    production_load_count = forms.IntegerField(required=False,label="Amount")
    production_price = forms.FloatField(label="Price")
    bonus = forms.DecimalField(initial=4)

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = ('payment_type','amount','date','description')
        widgets = {'date':DateInput()}
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
class RawInvoiceForm(forms.ModelForm):
    invoice_type = forms.ChoiceField(required=True,choices=Invoices.INVOICE_TYPE,label="Type")

    class Meta:
         model = Invoices
         fields= ('invoice_type','invoice_date','invoice_number')
         widgets = {'invoice_date':DateInput(),
                    'invoice_number': forms.TextInput(attrs={'placeholder': 'Invoice Number'})}
    def __init__(self, *args, **kwargs):
        super(RawInvoiceForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

class ItemsForm(forms.ModelForm):

    class Meta:
        model = Items

        fields= ['name','description','price','amount']
    def __init__(self, *args, **kwargs):
        super(ItemsForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

class IncomingInvoiceForm(forms.ModelForm):

    class Meta:
        model = IncomingInvoices
        fields= ['invoice_type','invoice_number','invoice_date',]
        widgets = {'invoice_date':DateInput(),
                   'invoice_number': forms.TextInput(attrs={'placeholder': 'Invoice Number'})}
    def __init__(self, *args, **kwargs):
        super(IncomingInvoiceForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
class IncomingInvoiceEditForm(forms.ModelForm):

    class Meta:
        model = IncomingInvoices
        fields= ['invoice_number','invoice_date']
        widgets = {'invoice_date':DateInput(),
                   'invoice_number': forms.TextInput(attrs={'placeholder': 'Invoice Number'})}
    def __init__(self, *args, **kwargs):
        super(IncomingInvoiceEditForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['description', 'document', ]
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
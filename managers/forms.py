from django import forms
from .models import *


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('id_product', 'name_product', 'type', 'producter', 'quantity', 'base_price', 'image')


class CustomForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class BillDetailForm(forms.ModelForm):
    class Meta:
        model = BillsDetail
        fields = ('id_staff', 'id_pro', 'quantity', 'promotion', )


class BillForm(forms.ModelForm):
    class Meta:
        model = Bills
        fields = ('id_bill', )


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

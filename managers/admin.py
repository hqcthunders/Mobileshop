from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(Products)
admin.site.register(Customer)
admin.site.register(Bills)
admin.site.register(BillsDetail)

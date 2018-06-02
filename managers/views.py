from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import date
import requests_html
import csv
from django.core import mail
# Create your views here.


def dashboard(request):
    if request.user.is_authenticated:
        data = {'Products': Products.objects.all()}
        return render(request, 'managers/dashboard.html', data)
    return redirect('login')


def add_products(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductsForm()
        return render(request, 'managers/products.html', {'form': form})


def edit_product(request, id):
    product = {'Products': Products.objects.get(id_product=id)}
    if request.method == 'POST':
        product.name_product = request.POST.get('name_product', '')
        product.quantity = request.POST.get('quantity', '')
        product.base_price = request.POST.get('base_price', '')
        product.save()
        return redirect('home')
    else:
        return render(request, 'managers/editproduct.html', product)


def delete(request, id):
    product = Products.objects.get(id_product=id)
    product.delete()
    return redirect('home')


def bill_custome(request):
    form1 = CustomForm()
    form2 = BillForm()
    form3 = BillDetailForm()
    if request.method == 'POST':
        id_customer = request.POST.get('id_customer', '')
        name_customer = request.POST.get('name_customer', '')
        gender = request.POST.get('gender', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        id_bill = request.POST.get('id_bill', '')
        id_staff = request.POST.get('id_staff', '')
        id_pro = request.POST.get('id_pro', '')
        quantity = int(request.POST.get('quantity', ''))
        promotion = int(request.POST.get('promotion', ''))
        # Add and save information custome
        custome = Customer.objects.create(id_customer=id_customer, name_customer=name_customer, gender=gender,
                           address=address, phone=phone, email=email)
        custome.save()
        # Add and save bill
        bill = Bills.objects.create(id_bill=id_bill, id_customer=custome)
        bill.save()
        #
        staff = Staff.objects.get(id=id_staff)
        pro = Products.objects.get(id_product=id_pro)
        # Add and save bill detail
        base_price = Products.objects.get(id_product=id_pro).base_price
        sum_price = base_price*quantity - (base_price*quantity*promotion / 100)
        bill_detail = BillsDetail.objects.create(id_bill=bill, id_staff=staff, id_pro=pro,
                                  quantity=quantity, promotion=promotion, sum_price=sum_price)
        bill_detail.save()
        return render(request, 'managers/bills.html', {
            'customer': form1,
            'bill': form2,
            'billdetail': form3,
            'BillDetails': BillsDetail.objects.all()
        })
    else:
        return render(request, 'managers/bills.html', {
            'customer': form1,
            'bill': form2,
            'billdetail': form3,
            'BillDetails': BillsDetail.objects.all()
        })


def add_staff(request):
    form = StaffForm()
    if request.method == "POST":
        staff = StaffForm(request.POST)
        if staff.is_valid():
            staff.save()
            return render(request, 'managers/addstaff.html', {'form': form, 'Staffs': Staff.objects.all()})
    else:
        return render(request, 'managers/addstaff.html', {'form': form, 'Staffs': Staff.objects.all()})


def enemy(request):
    session = requests_html.HTMLSession()
    res = session.get("https://www.thegioididong.com/")
    products = res.html.find("div.item > a > h3")[:10]
    prices = res.html.find("div.item > a > div.price > strong")[:10]
    data = [(product.text, price.text) for product, price in zip(products, prices)]
    return render(request, 'managers/enemy.html', {'Products': data})


def csv_to_mail(request):
    bill_detail = BillsDetail.objects.all()
    with open("statistical.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["Ngay lap", "Khach Hang", "Phone", "Ten Hang", "So luong", "Tong gia tri"])
        for bill in bill_detail:
            writer.writerow([bill.id_bill.date_of_bill, bill.id_bill.id_customer, bill.id_bill.id_customer.phone,
                             bill.id_pro.name_product, bill.quantity, bill.sum_price])
    try:
        connection = mail.get_connection()
        connection.open()
        text = "Bao cao cua hang trong ngay"
        mail_ = mail.EmailMessage("Bao cao ngay {}".format(str(date.today())), text, "tintuc.ks.is@gmail.com",
                                  ["clinkin.ks.is@gmail.com"])
        mail_.attach_file("statistical.csv")
        mail_.send()
        connection.close()
    except:
        return "Erro"
    return redirect('home')
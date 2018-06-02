from django.db import models

# Create your models here.


class Department(models.Model):
    id_department = models.CharField(max_length=8, primary_key=True)
    name_department = models.CharField(max_length=30)

    def __str__(self):
        return self.name_department


class Staff(models.Model):
    name_staff = models.CharField(max_length=30)
    birth = models.DateField(null=False)
    phone = models.CharField(max_length=12)
    id_number = models.CharField(max_length=12)
    address = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_staff


class Products(models.Model):
    id_product = models.CharField(max_length=8, primary_key=True)
    name_product = models.CharField(max_length=30)
    type = models.CharField(max_length=20)
    producter = models.CharField(max_length=20)
    quantity = models.IntegerField(null=False)
    base_price = models.FloatField(null=False)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name_product


class Customer(models.Model):
    Gender_choice = (('M', 'Male'), ('FM', 'Female'))
    id_customer = models.CharField(max_length=8, primary_key=True)
    name_customer = models.CharField(max_length=30)
    gender = models.CharField(max_length=5, choices=Gender_choice)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name_customer


class Bills(models.Model):
    id_bill = models.CharField(max_length=8, primary_key=True)
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_of_bill = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id_bill


class BillsDetail(models.Model):
    id_bill = models.ForeignKey(Bills, on_delete=models.CASCADE)
    id_staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    id_pro = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    promotion = models.FloatField(null=False)
    sum_price = models.FloatField(null=True)

    def __str__(self):
        return "{} of customer {}".format(self.id_bill.id_bill, self.id_bill.id_customer)


class Store(models.Model):
    id_pro = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    date_add = models.DateField(auto_now_add=True)

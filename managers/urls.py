from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('login/', auth_views.login, {'template_name': 'managers/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path('addproduct/', views.add_products, name='add'),
    path('edit/<slug:id>/', views.edit_product, name='edit'),
    path('delete/<slug:id>/', views.delete, name='delete'),
    path('bills/', views.bill_custome, name='bill'),
    path('addstaff/', views.add_staff, name='add_staff'),
    path('enemy/', views.enemy, name="enemy"),
    path('sendcsv/', views.csv_to_mail, name="csv")
]
from django.shortcuts import render, redirect
from .models import Customer
from django.shortcuts import render



def initialize_customer_data(request):
    cust = Customer.objects.first()
    return redirect('home')

def customer_options(request):
    return render(request, 'customer/customer_options.html')

def customer_login(request):
    return render(request, 'customer/customer_login.html') 

def customer_signup(request):
    return render(request, 'customer/customer_signup.html')
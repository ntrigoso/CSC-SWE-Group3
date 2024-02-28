from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import Customer
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customer.backends import EmailAuthenticationBackend


def initialize_customer_data(request):
    cust = Customer.objects.first()
    return redirect('home')

def customer_options(request):
    return render(request, 'customer/customer_options.html')

def customer_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please login.')
            return redirect('customer-login')
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            Customer.objects.create(user=user, email=email)
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('customer-login')
    return render(request, 'customer/customer_signup.html')

redirect_authenticated_user = True

def customer_login(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to authenticate user
        user = authenticate(request, username=email, password=password) 

        # If able to authenticate, log user in and redirect
        if user is not None:
            login(request, user)
            return redirect('customer-dashboard')
        # Couldn't authenticate, show error message
        else:
            context = {'error': 'Invalid credentials'}
            return render(request, 'customer/customer_login.html', context)
            
    # Render blank login form            
    else:
        form = AuthenticationForm()
        return render(request, 'customer/customer_login.html', {'form': form}) 
    

def customer_profile(request):
    return render(request, 'customer/customer_profile.html')

@login_required
def customer_dashboard(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        weight = request.POST.get('weight')
        
        # Create package object and save to db
        package = Package.objects.create(
            name=name,
            weight=weight
        )
        
        # Redirect to view package details
        return redirect('package-detail', package.id)

    # Display dashboard 
    return render(request, 'customer/customer_dashboard.html') 
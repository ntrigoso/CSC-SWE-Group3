from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import Customer
from business.models import Package, Shipment
from business.forms import PackageForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from customer.backends import EmailAuthenticationBackend
from django.contrib import messages


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
            error_message = 'Invalid credentials'
            return render(request, 'customer/customer_login.html', {'error_message': error_message})

    # Render blank login form
    return render(request, 'customer/customer_login.html')
    

def customer_profile(request):
    customer = Customer.objects.get(user_id=request.user.id)
    context = {
        'customer': customer
    }
    return render(request, 'customer/customer_profile.html', context) 

counter = 1

def generate_order_number():
    global counter
    order_number = 'ORD' + str(counter)
    counter += 1
    return order_number

@login_required
def customer_dashboard(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            # Create a new Shipment instance
            shipment = Shipment.objects.create(
                customer=request.user.customer,
                order_number=generate_order_number(),
                status='Pending',
                # Set other shipment fields as needed
            )

            package = form.save(commit=False)
            package.customer = request.user.customer
            package.shipment_id = shipment.id  # Set the shipment_id for the package
            package.save()

            # Redirect or display success message
            return redirect('package-detail', package.package_id)
    else:
        form = PackageForm()

    context = {
        'form': form,
    }
    active_orders = Shipment.objects.filter(customer=request.user.customer, status__in=['Pending', 'In Progress'])
    form = PackageForm()
    active_orders = Shipment.objects.filter(
        customer=request.user.customer, 
        status__in=['Pending', 'In Progress']
    ).distinct()
    context = {
        'form': form,
        'active_orders': active_orders,
    }
    return render(request, 'customer/customer_dashboard.html', context)

@login_required
def customer_service(request):
    if request.method == 'POST':
        order_id = request.POST.get('order')
        complaint = request.POST.get('complaint')

        try:
            order = Shipment.objects.get(id=order_id, customer=request.user.customer)
            # You can handle the complaint logic here, e.g., send an email, update the order status, etc.
            messages.success(request, 'Your complaint has been received. We will get back to you shortly.')
        except Shipment.DoesNotExist:
            messages.error(request, 'Invalid order selected.')

    return redirect('customer-dashboard')
from .models import CustomerServiceMessage
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Package, Order, Feedback
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from customer.backends import EmailAuthenticationBackend
from .forms import OrderForm, ComplaintForm, FeedbackForm
from django.http import JsonResponse
from tracking.models import Shipment
from geopy.distance import geodesic
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Customer, Admin
from django.shortcuts import redirect
import random
import string



@login_required
def submit_customer_service_message(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user_id=request.user.id)
        message = request.POST.get('message')
        CustomerServiceMessage.objects.create(
            customer=customer,
            message=message,
            status='Open'
        )
        return redirect('customer-dashboard')
    return redirect('customer-dashboard')


print('Trying to reverse URL: business-portal')
def generate_temporary_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            customer = Customer.objects.get(email=email)
            temporary_password = generate_temporary_password()
            customer.user.set_password(temporary_password)
            customer.user.save()
            subject = 'Temporary Password'
            message = f'Your temporary password is: {temporary_password}'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            messages.success(request, 'A temporary password has been sent to your email.')
            return redirect('customer-login')
        except Customer.DoesNotExist:
            messages.error(request, 'No account found with that email.')
    return render(request, 'customer/forgot_password.html')


@login_required
def customer_logout(request):
    logout(request)
    request.session.flush()
    return redirect('home')

def initialize_customer_data(request):
    cust = Customer.objects.first()
    return redirect('home')


def customer_options(request):
    return render(request, 'customer/customer_options.html')


def customer_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please login.')
            return redirect('customer-login')
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            if user_type == 'customer':
                Customer.objects.create(user_id=user.id, email=email)
            elif user_type == 'admin':
                Admin.objects.create(user_id=user.id, email=email)
            else:
                messages.error(request, 'Invalid user type.')
                return redirect('customer-signup')
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('customer-login')
    return render(request, 'customer/customer_signup.html')


redirect_authenticated_user = True


def customer_login(request):
    if request.user.is_authenticated:
        try:
            admin = Admin.objects.get(user_id=request.user.id)
            request.session['user_type'] = 'admin'
            return redirect('business:business-portal')
        except Admin.DoesNotExist:
            request.session['user_type'] = 'customer'
            return redirect('customer-dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            try:
                admin = Admin.objects.get(user_id=user.id)
                request.session['user_type'] = 'admin'
                return redirect('business:business-portal')
            except Admin.DoesNotExist:
                request.session['user_type'] = 'customer'
                return redirect('customer-dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'customer/customer_login.html')




@login_required
def customer_profile(request):
    customer = Customer.objects.get(user_id=request.user.id)
    context = {
        'customer': customer
    }
    return render(request, 'customer/customer_profile.html', context)

@login_required
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(user_id=request.user.id)
            order = Order.objects.create(
                customer=customer,
                package_dimensions=form.cleaned_data['package_dimensions'],
                package_weight=form.cleaned_data['package_weight'],
                pickup_or_dropoff=form.cleaned_data['pickup_or_dropoff'],
                pickup_address=form.cleaned_data['pickup_address'],
                delivery_address=form.cleaned_data['delivery_address'],
                shipping_type=form.cleaned_data['shipping_type'],
                estimated_cost=calculate_estimated_cost(
                    form.cleaned_data['package_dimensions'],
                    form.cleaned_data['package_weight'],
                    form.cleaned_data['shipping_type']
                )['total'],
                status='Processing'
            )
            Shipment.objects.create(
                tracking_number=generate_tracking_number(),
                package_description=f'Order #{order.order_number}',
                pickup_address=form.cleaned_data['pickup_address'],
                delivery_address=form.cleaned_data['delivery_address'],
                customer=customer,
                status='Processing'
            )
            return redirect('customer-dashboard')
    else:
        form = OrderForm()
    return render(request, 'customer/order_form.html', {'form': form})



@login_required
def customer_dashboard(request):
    if request.session.get('user_type') != 'customer':
        return redirect('customer-login')
    try:
        customer = Customer.objects.get(user_id=request.user.id)
    except Customer.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('customer-login')

    active_orders = Order.objects.filter(customer=customer, status='Processing')
    past_orders = Order.objects.filter(customer=customer).exclude(status='Processing')
    customer_service_messages = CustomerServiceMessage.objects.filter(customer=customer)

    order_form = OrderForm()

    if request.method == 'POST':
        if 'order_form' in request.POST:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = Order.objects.create(
                    customer=customer,
                    package_dimensions=order_form.cleaned_data['package_dimensions'],
                    package_weight=order_form.cleaned_data['package_weight'],
                    pickup_or_dropoff=order_form.cleaned_data['pickup_or_dropoff'],
                    estimated_cost=calculate_estimated_cost(
                        order_form.cleaned_data['package_dimensions'],
                        order_form.cleaned_data['package_weight'],
                        order_form.cleaned_data['pickup_or_dropoff']
                    )['total'],
                    status='Processing'
                )
                Shipment.objects.create(
                    tracking_number=generate_tracking_number(),
                    package_description=f'Order #{order.order_number}',
                    pickup_address=customer.address,
                    delivery_address=customer.address,
                    customer=customer,
                    status='Processing'
                )
                return redirect('customer-dashboard')
        elif 'customer_service_form' in request.POST:
            message = request.POST.get('message')
            CustomerServiceMessage.objects.create(
                customer=customer,
                message=message,
                status='Open'
            )
            return redirect('customer-dashboard')

    context = {
        'order_form': order_form,
        'active_orders': active_orders,
        'past_orders': past_orders,
        'customer_service_messages': customer_service_messages,
        'customer': customer
    }
    return render(request, 'customer/customer_dashboard.html', context)



def calculate_estimated_cost(package_dimensions, package_weight, shipping_type):
    # Implement a realistic shipping cost calculation based on the package dimensions, weight, and shipping type
    if shipping_type == 'ground':
        shipping_cost = 10.0
    elif shipping_type == 'priority':
        shipping_cost = 20.0
    elif shipping_type == 'nextDay':
        shipping_cost = 30.0
    else:
        shipping_cost = 0.0

    base_cost = package_weight * 0.5
    handling_cost = 5.0
    subtotal = base_cost + shipping_cost + handling_cost
    tax = subtotal * 0.1
    total = subtotal + tax

    return {
        'shipping': shipping_cost,
        'handling': handling_cost,
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    }


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            customer = Customer.objects.get(email=email)
            user = User.objects.get(id=customer.user_id)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(f'/customer/reset-password/{uid}/{token}/')
            subject = 'Reset Your Password'
            message = render_to_string('customer/reset_password_email.html', {
                'user': user,
                'reset_url': reset_url
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            messages.success(request, 'Password reset email has been sent.')
            return redirect('customer-login')
        except Customer.DoesNotExist:
            messages.error(request, 'No account found with that email.')
    return render(request, 'customer/forgot_password.html')


@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(user_id=request.user.id)
            feedback = form.save(commit=False)
            feedback.customer = customer
            feedback.save()
            messages.success(request, 'Feedback submitted successfully.')
            return redirect('customer-dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'customer/feedback_form.html', {'form': form})


def get_shipping_cost(shipping_type, address):
    # Implement a realistic shipping cost calculation based on the address
    # and the shipping type
    if shipping_type == 'ground':
        return 10.0
    elif shipping_type == 'priority':
        return 20.0
    elif shipping_type == 'nextDay':
        return 30.0
    else:
        return 0.0


def customer_logout(request):
    logout(request)
    return redirect('home')


def calculate_estimated_cost(height, width, length, shipping_type):
    volume = height * width * length
    base_cost = volume * 0.5
    shipping_cost = get_shipping_cost(shipping_type)
    handling_cost = 5.0
    subtotal = base_cost + shipping_cost + handling_cost
    tax = subtotal * 0.1
    total = subtotal + tax

    return {
        'shipping': shipping_cost,
        'handling': handling_cost,
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    }


def get_shipping_cost(shipping_type):
    if shipping_type == 'ground':
        return 10.0
    elif shipping_type == 'priority':
        return 20.0
    elif shipping_type == 'nextDay':
        return 30.0
    else:
        return 0.0


def process_complaint(complaint):
    pass



@login_required
def customer_profile(request):
    customer = Customer.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        # Update customer profile information
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.address = request.POST.get('address')
        customer.phone = request.POST.get('phone')
        customer.save()
        messages.success(request, 'Profile updated successfully.')
    return render(request, 'customer/customer_profile.html', {'customer': customer})


@login_required
def admin_profile(request):
    customer = Customer.objects.get(user_id=request.user.id)
    if customer.is_admin:
        if request.method == 'POST':
            # Update admin profile information
            customer.first_name = request.POST.get('first_name')
            customer.last_name = request.POST.get('last_name')
            customer.address = request.POST.get('address')
            customer.phone = request.POST.get('phone')
            customer.save()
            messages.success(request, 'Profile updated successfully.')
        return render(request, 'admin/admin_profile.html', {'customer': customer})
    else:
        return redirect('customer-profile')

@login_required

def business_portal(request):
    user_type = request.session.get('user_type')
    if user_type == 'admin':
        try:
            admin = Admin.objects.get(user_id=request.user.id)
            return render(request, 'business/business_portal.html')
        except Admin.DoesNotExist:
            messages.error(request, 'This account is not associated with an admin.')
            return redirect('customer-login')
    else:
        messages.error(request, 'You are not authorized to access the business portal.')
        return redirect('customer-dashboard')


@login_required
def track_shipment(request):
    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number')
        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number, customer__user_id=request.user.id)
            return render(request, 'customer/shipment_status.html', {'shipment': shipment})
        except Shipment.DoesNotExist:
            return render(request, 'customer/shipment_status.html', {'error': 'Invalid tracking number.'})
    return render(request, 'customer/track_shipment.html')
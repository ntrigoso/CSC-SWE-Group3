from django.shortcuts import render, redirect
from .forms import QuoteRequestForm
from .models import QuoteRequest
from .utils import calculate_estimated_cost

import math

def calculate_distance(zip1, zip2):
    # Implement a function to calculate the distance between two zip codes
    # You can use a third-party library or API for this
    # For the sake of this example, let's assume a simple calculation
    return abs(int(zip1) - int(zip2)) * 10  # Distance in miles

def calculate_estimated_cost(package_dimensions, package_weight, pickup_zip, delivery_zip, shipping_type):
    distance = calculate_distance(pickup_zip, delivery_zip)
    base_cost = package_weight * 0.5  # $0.50 per pound
    shipping_cost = distance * 0.25  # $0.25 per mile

    if shipping_type == 'ground':
        shipping_cost *= 1.0  # No additional cost for ground shipping
    elif shipping_type == 'priority':
        shipping_cost *= 1.5  # 50% additional cost for priority shipping
    elif shipping_type == 'nextDay':
        shipping_cost *= 2.0  # 100% additional cost for next-day shipping

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

def quote_request(request):
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote_request = form.save()
            estimate_breakdown = calculate_estimated_cost(
                quote_request.package_dimensions,
                quote_request.package_weight,
                quote_request.pickup_address[:5],  # Assuming zip code is the first 5 characters
                quote_request.delivery_address[:5],
                quote_request.shipping_type
            )
            return render(request, 'quote/quote_form.html', {'form': form, 'estimate_breakdown': estimate_breakdown})
    else:
        form = QuoteRequestForm()
    return render(request, 'quote/quote_form.html', {'form': form})

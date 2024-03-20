import math

def calculate_estimated_cost(dimensions, weight, pickup_zip, delivery_zip, shipping_type):
    # Implement your cost calculation logic here
    # This is a simple example, you may want to add more complex calculations
    base_cost = weight * 0.5
    shipping_cost = get_shipping_cost(shipping_type, pickup_zip, delivery_zip)
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

def get_shipping_cost(shipping_type, pickup_zip, delivery_zip):
    # Implement your shipping cost logic here
    # This is a simple example, you may want to add more complex calculations
    if shipping_type == 'ground':
        return 10.0
    elif shipping_type == 'priority':
        return 20.0
    elif shipping_type == 'nextDay':
        return 30.0
    else:
        return 0.0

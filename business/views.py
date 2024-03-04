from django.shortcuts import render, get_object_or_404
from .models import Package, Shipment
from django.contrib import messages
from django.shortcuts import redirect

def home(request):
  return render(request, 'home.html') 

def business_portal(request):
    return render(request, 'business/business_portal.html')


def inventory_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        packages = Package.objects.filter(customer=customer)
        shipments = Shipment.objects.filter(customer=customer).distinct()
    else:
        packages = []
        shipments = []

    context = {
        'packages': packages,
        'shipments': shipments,
        'customer': customer,
    }
    return render(request, 'business/business_portal.html', context)


def package_detail(request, package_id):
    package = get_object_or_404(Package, package_id=package_id)
    context = {
        'package': package,
    }
    return render(request, 'business/package_detail.html', context)


def dispatch_package(request, package_id):
    package = get_object_or_404(Package, package_id=package_id)
    # Add logic to dispatch the package to the queue in the Routes tab
    messages.success(request, f'Package {package.package_id} has been dispatched.')
    return redirect('business_portal')

def deny_package(request, package_id):
    package = get_object_or_404(Package, package_id=package_id)
    # Add logic to deny the package and notify the customer
    messages.success(request, f'Package {package.package_id} has been denied.')
    return redirect('business_portal')

def dispatch_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    # Add logic to dispatch the shipment to the queue in the Routes tab
    messages.success(request, f'Shipment {shipment.order_number} has been dispatched.')
    return redirect('business_portal')

def deny_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    # Add logic to deny the shipment and notify the customer
    messages.success(request, f'Shipment {shipment.order_number} has been denied.')
    return redirect('business_portal')
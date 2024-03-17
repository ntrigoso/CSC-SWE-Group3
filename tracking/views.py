from customer.models import Shipment

def package_status(request):
    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number')
        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
            return render(request, 'tracking/package_status.html', {'shipment': shipment})
        except Shipment.DoesNotExist:
            return render(request, 'tracking/package_status.html', {'error': 'Invalid tracking number.'})
    return render(request, 'tracking/package_status.html')

# inventory/views.py

from django.shortcuts import render
from .models import Stock

def inventory_view(request):
    stocks = Stock.objects.all()
    context = {
        'stocks': stocks 
    }
    return render(request, 'business/business_portal.html', context)
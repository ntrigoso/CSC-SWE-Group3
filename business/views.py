from django.shortcuts import render

def home(request):
  return render(request, 'home.html') 

def business_portal(request):
    return render(request, 'business/business_portal.html')


def inventory_view(request):
    return HttpResponse("This is the inventory view.")
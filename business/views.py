from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from customer.models import Admin
from django.contrib import messages



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


def home(request):
  return render(request, 'home.html') 

def business_portal(request):
    try:
        admin = Admin.objects.get(user_id=request.user.id)
        return render(request, 'business/business_portal.html')
    except Admin.DoesNotExist:
        return redirect('customer-login')

def inventory_view(request):
    packages = Package.objects.all()
    context = {
        'packages': packages 
    }
    return render(request, 'business/business_portal.html', context)
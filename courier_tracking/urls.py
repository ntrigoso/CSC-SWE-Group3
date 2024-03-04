from django.contrib import admin
from django.urls import path, include
from business.views import home  
from django.urls import reverse
from customer.views import customer_options, customer_login, customer_signup, customer_dashboard


urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('business/', include('business.urls'), name='business_portal'),
    path('', home, name='home'),  
    path('business/inventory/', include('inventory.urls')), 
    path('', customer_options, name='customer-options'),
    path('login/', customer_login, name='customer-login'), 
    path('signup/', customer_signup, name='customer-signup'),
    path('customer/dashboard/', customer_dashboard, name='customer-dashboard'),
]

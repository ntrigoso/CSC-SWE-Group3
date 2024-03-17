from django.contrib import admin
from django.urls import path, include
from business.views import home  
from customer.views import customer_options, customer_login, customer_signup, customer_dashboard
from quote.views import quote_request
from tracking.views import package_status
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('business/', include('business.urls')),
    path('business/inventory/', include('inventory.urls')),
    path('login/', customer_login, name='customer-login'), 
    path('dashboard/', customer_dashboard, name='customer-dashboard'),
    path('', home, name='home'),  
    path('signup/', customer_signup, name='customer-signup'),
    path('quote/', quote_request, name='quote-request'),
    path('track/', package_status, name='package-status'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('customer/options/', customer_options, name='customer-options'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
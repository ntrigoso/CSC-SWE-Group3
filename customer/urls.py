from django.urls import path
from .views import customer_login, initialize_customer_data, customer_signup, customer_options

urlpatterns = [
    path('', customer_options, name='customer-options'),
    path('signup/', customer_signup, name='customer-signup'),
    path('login/', customer_login, name='customer-login'),
    path('initialize-data/', initialize_customer_data, name='initialize-customer-data'),
    path('login/', customer_login, name='customer-login'),
    
]

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import customer_login, initialize_customer_data, customer_signup, customer_options, customer_profile, customer_dashboard, customer_logout, place_order, submit_feedback, forgot_password

urlpatterns = [
    path('', customer_options, name='customer-options'),
    path('signup/', customer_signup, name='customer-signup'),
    path('login/', customer_login, name='customer-login'),
    path('initialize-data/', initialize_customer_data, name='initialize-customer-data'),
    path('profile/', customer_profile, name='customer-profile'),
    path('dashboard/', customer_dashboard, name='customer-dashboard'),
    path('logout/', customer_logout, name='customer-logout'),
    path('place-order/', place_order, name='place-order'),
    path('submit-feedback/', submit_feedback, name='submit-feedback'),
    path('forgot-password/', forgot_password, name='forgot-password'),
]
from django.urls import path  
from . import views

app_name = 'business'

urlpatterns = [
    path('', views.home, name='home'),
    path('business-portal/', views.business_portal, name='business-portal'),
    # path('business/', views.business_portal, name='business_portal'),
    path('inventory/', views.inventory_view, name='inventory'),
]
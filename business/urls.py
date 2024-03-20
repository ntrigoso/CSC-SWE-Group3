from django.urls import path  
from .views import business_portal
from . import views

app_name = 'business'

urlpatterns = [
    path('', views.home, name='home'),
    path('portal/', views.business_portal, name='business-portal'),
    path('inventory/', views.inventory_view, name='inventory'),
]
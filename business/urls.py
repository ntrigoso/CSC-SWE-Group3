from django.urls import path  
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('business/', views.business_portal, name='business_portal'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('packages/<int:package_id>/', views.package_detail, name='package-detail'),
    path('dispatch-package/<int:package_id>/', views.dispatch_package, name='dispatch-package'),
    path('deny-package/<int:package_id>/', views.deny_package, name='deny-package'),
    path('dispatch-shipment/<int:shipment_id>/', views.dispatch_shipment, name='dispatch-shipment'),
    path('deny-shipment/<int:shipment_id>/', views.deny_shipment, name='deny-shipment'),
]
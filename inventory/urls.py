from django.urls import path
from . import views
from django.contrib.auth.models import User 

urlpatterns = [
    path('inventory/', views.inventory_view, name='inventory'),
]
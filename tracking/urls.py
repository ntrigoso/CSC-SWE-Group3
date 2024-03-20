from django.urls import path
from .views import package_status

urlpatterns = [
    path('package-status/', package_status, name='package-status'),
]
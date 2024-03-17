from django.contrib import admin
from .models import Package, Shipment, Driver, Vehicle

admin.site.register(Package)
admin.site.register(Shipment) 
admin.site.register(Driver)
admin.site.register(Vehicle)
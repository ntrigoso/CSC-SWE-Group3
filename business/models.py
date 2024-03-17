from django.db import models


class Package(models.Model):
    package_id = models.AutoField(primary_key=True)
    shipment_id = models.IntegerField()
    package_description = models.TextField(null=True, blank=True)
    package_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    package_dimensions = models.CharField(max_length=255, null=True, blank=True)
    package_status = models.CharField(max_length=50, null=True, blank=True)

class Shipment(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=50, null=True, blank=True)
    customer_id = models.IntegerField(null=True, blank=True)
    order_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    shipment_date = models.DateField(null=True, blank=True)
    driver_id = models.IntegerField(null=True, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    driver_name = models.CharField(max_length=100, null=True, blank=True)
    vehicle_id = models.IntegerField(null=True, blank=True)

class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    vehicle_model = models.CharField(max_length=100, null=True, blank=True)
    vehicle_plate = models.CharField(max_length=20, null=True, blank=True)
    vehicle_status = models.CharField(max_length=50, null=True, blank=True)
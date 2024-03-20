from django.db import models

class Shipment(models.Model):
    tracking_number = models.CharField(max_length=20, unique=True)
    package_description = models.TextField(null=True, blank=True)
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='Processing')
    updated_at = models.DateTimeField(auto_now=True)


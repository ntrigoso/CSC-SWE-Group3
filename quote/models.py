from django.db import models

class QuoteRequest(models.Model):
    package_dimensions = models.CharField(max_length=50)
    package_weight = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    shipping_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

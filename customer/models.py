from django.db import models
from inventory.models import Stock

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True) 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
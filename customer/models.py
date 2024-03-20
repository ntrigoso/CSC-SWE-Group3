from django.db import models
from inventory.models import Stock
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class Customer(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    def check_password(self, raw_password):
        return check_password(raw_password, str(self.user_id))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CustomerServiceMessage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Open')


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    def __str__(self):
        return self.business_name


class Package(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    height = models.IntegerField()
    width = models.IntegerField()
    length = models.IntegerField()
    address = models.CharField(max_length=255)
    shipping_type = models.CharField(max_length=20)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Processing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Package #{self.id}"



class Shipment(models.Model):
    tracking_number = models.CharField(max_length=20, unique=True)
    package_description = models.TextField(null=True, blank=True)
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='Processing')
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    package_dimensions = models.CharField(max_length=20)
    package_weight = models.DecimalField(max_digits=5, decimal_places=2)
    pickup_or_dropoff = models.CharField(max_length=10)
    pickup_address = models.CharField(max_length=255, blank=True, null=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Processing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)




class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
  list_display = ['first_name', 'last_name', 'stock']

admin.site.register(Customer, CustomerAdmin)
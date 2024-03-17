from django.contrib.auth.backends import BaseBackend
from .models import Customer

class EmailAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            customer = Customer.objects.get(email=username)
            if customer.check_password(password):
                return customer.user_id
            return None
        except Customer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Customer.objects.get(user_id=user_id)
        except Customer.DoesNotExist:
            return None
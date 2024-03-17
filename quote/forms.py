from django import forms
from .models import QuoteRequest

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['package_dimensions', 'package_weight', 'pickup_address', 'delivery_address', 'shipping_type']

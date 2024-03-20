from django import forms
from .models import Customer, Feedback
from .models import Order

SHIPPING_CHOICES = [
    ('ground', 'Ground'),
    ('priority', 'Priority'),
    ('nextDay', 'Next Day'),
]

class OrderForm(forms.ModelForm):
    shipping_type = forms.ChoiceField(choices=SHIPPING_CHOICES)

    class Meta:
        model = Order
        fields = ['package_dimensions', 'package_weight', 'pickup_or_dropoff', 'pickup_address', 'delivery_address', 'shipping_type']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment']

class ComplaintForm(forms.Form):
    complaint = forms.CharField(widget=forms.Textarea)
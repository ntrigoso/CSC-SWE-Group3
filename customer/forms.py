from django import forms
from .models import Customer, Feedback


class OrderForm(forms.Form):
    pickup_or_dropoff = forms.ChoiceField(choices=[('pickup', 'Pickup'), ('dropoff', 'Drop-off')], widget=forms.Select())
    package_dimensions = forms.CharField(max_length=20, help_text='Enter dimensions in LxWxH format (e.g., 12x6x4)')
    package_weight = forms.DecimalField(max_digits=5, decimal_places=2, help_text='Enter weight in pounds')

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment']

class ComplaintForm(forms.Form):
    complaint = forms.CharField(widget=forms.Textarea)
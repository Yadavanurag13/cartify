# forms.py
from django import forms
from .models import Customer

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),  # Make email read-only
        }

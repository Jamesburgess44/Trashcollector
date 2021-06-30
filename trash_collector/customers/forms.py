from django import forms
from .models import Customer


class customer_forms(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

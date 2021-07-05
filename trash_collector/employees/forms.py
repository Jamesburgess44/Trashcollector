from django import forms
from .models import Employee


class customer_forms(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'employee_zip_code',)

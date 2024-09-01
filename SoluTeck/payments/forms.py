from django import forms
from .models import TuitionFee

class TuitionFeeForm(forms.ModelForm):
    class Meta:
        model = TuitionFee
        fields = ['student', 'amount', 'due_date', 'payment_method']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
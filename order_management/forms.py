from django import forms
from .models import Order, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status'] 
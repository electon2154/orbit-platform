from django import forms
from .models import Product, Category
from user_accounts.models import CompanyProfile

class ProductForm(forms.ModelForm):
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        label='السعر',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number',
            'step': '0.01',
            'min': '0'
        })
    )
    
    stock = forms.IntegerField(
        min_value=0,
        label='المخزون',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number',
            'min': '0'
        })
    )

    class Meta:
        model = Product
        fields = [
            'name', 'code', 'description', 'price', 'stock',
            'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'اسم المنتج',
            'code': 'رمز المنتج',
            'description': 'الوصف',
            'image': 'الصورة',
        } 
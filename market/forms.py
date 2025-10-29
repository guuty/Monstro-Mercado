from django import forms
from market.models import Product  


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        
        fields = ['title', 'description', 'marca', 'price', 'stock', 'image', 'active'] 
        
        # Widgets para aplicar clases de Bootstrap
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o título del producto'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el producto en detalle'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Sony, Samsung, Genérica'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # Checkbox
            # 'image' no necesita widget si es ImageField
        }
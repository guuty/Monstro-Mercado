from django import forms
from productos.models import Producto

# 1. FORMULARIO PARA CREAR/EDITAR PRODUCTOS (ProductForm)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        
        fields = [
            'nombre', 'descripcion', 'precio', 'imagen', 'stock', 'marca',  # <-- CORREGIDO
             'category', 'condition'
        ] 
        
        labels = {
            'nombre': 'Nombre del Producto', 
            'descripcion': 'Descripción', 
            'precio': 'Precio', 
            'imagen': 'Imagen', 
            'stock': 'Stock Disponible',
            'marca': 'Marca', 
            'category': 'Categoría', 
            'condition': 'Condición',
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Coca Cola 2.25L'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el producto...'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Coca Cola'}),
            'category': forms.Select(attrs={'class': 'form-select'}), 
            'condition': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        } 


# 2. FORMULARIO PARA FILTRAR PRODUCTOS (ProductFilterForm)

CATEGORY_CHOICES = [
    ('', 'Todas las categorías'),
    ('almacen', 'Almacén'),
    ('bebidas', 'Bebidas'),
    ('lacteos', 'Lácteos y Huevos'),
    ('carnes', 'Carnes y Pescados'),
    ('frutas', 'Frutas y Verduras'),
    ('panaderia', 'Panadería'),
    ('limpieza', 'Limpieza'),
    ('higiene', 'Higiene Personal'),
    ('congelados', 'Congelados'),
    ('snacks', 'Snacks y Golosinas'),
    ('desayuno', 'Desayuno y Cereales'),
]

BRAND_CHOICES = [
    ('', 'Todas las marcas'),
    ('Coca Cola', 'Coca Cola'),
    ('Quilmes', 'Quilmes'),
    ('La Serenísima', 'La Serenísima'),
    ('Arcor', 'Arcor'),
    ('Bagley', 'Bagley'),
    ('Marolio', 'Marolio'),
    ('Molinos', 'Molinos'),
    ('Knorr', 'Knorr'),
    ('Hellmanns', 'Hellmann\'s'),
    ('Nescafé', 'Nescafé'),
    ('Cindor', 'Cindor'),
    ('Milka', 'Milka'),
    ('Oreo', 'Oreo'),
    ('Fargo', 'Fargo'),
    ('La Campagnola', 'La Campagnola'),
]

CONDITION_CHOICES = [
    ('', 'Todos los tipos'),
    ('new', 'Nuevo'),
    ('used', 'Usado'),
]


class ProductFilterForm(forms.Form):
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        label='Categoría'
    )

    marca = forms.ChoiceField(
        choices=BRAND_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        label='Marca'
    )
    
    condition = forms.ChoiceField(
        choices=CONDITION_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Tipo'
    )
    
    price_min = forms.DecimalField(
        label='Min',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Min'})
    )
    
    price_max = forms.DecimalField(
        label='Max',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Max'})
    )
from django import forms
from market.models import Product 

# 1. FORMULARIO PARA CREAR/EDITAR PRODUCTOS (ProductForm)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        
        # Campos utilizados en el formulario de publicación
        fields = [
            'title', 'description', 'price', 'image', 'stock', 'marca',
            'category', 'condition', 'active'
        ] 
        
        # Traducciones de las etiquetas (Labels)
        labels = {
            'title': 'Título', 
            'description': 'Descripción', 
            'price': 'Precio', 
            'image': 'Imagen', 
            'stock': 'Cantidad', 
            'marca': 'Marca', 
            'category': 'Categoría', 
            'condition': 'Condición', 
            'active': 'Activo (Disponible para la venta)', 
        }
        
        # Widgets para aplicar estilos de Bootstrap
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Joystick PS4 Camuflado'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el estado, uso, etc.'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}), # Usamos ClearableFileInput para imágenes
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Sony'}),

            # Select para Categoría (Dropdown)
            'category': forms.Select(attrs={'class': 'form-select'}), 
            
            # RadioSelect para Condición (Botones de radio)
            'condition': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            
            # Checkbox para Activo
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        } 



# 2. FORMULARIO PARA FILTRAR PRODUCTOS (ProductFilterForm)


# Definimos las opciones para el filtro (deben coincidir con el modelo si es necesario)
CONDITION_CHOICES = [
    ('', 'Todos los tipos'), # Opción por defecto
    ('new', 'Nuevo'),
    ('used', 'Usado'),
]

# Obtenemos las opciones de categoría del modelo Product y añadimos el default 'Todas'
CATEGORY_CHOICES = [('', 'Todas las categorías')] + list(Product.CATEGORY_CHOICES)

# Opciones de Marca (Este listado debe ser alimentado dinámicamente en producción, pero lo mantenemos simple por ahora)
# Usamos un conjunto para evitar duplicados si usas las marcas del modelo:
# available_brands = Product.objects.values_list('marca', flat=True).distinct()
BRAND_CHOICES = [
    ('', 'Todas las marcas'),
    ('Sony', 'Sony'),
    ('Philips', 'Philips'),
    ('360 fitness', '360 fitness'),
    ('Ombu', 'Ombu'),
    ('Genérico', 'Genérico'),
]


class ProductFilterForm(forms.Form):
    # Campo Categoria
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        label='Categoría'
    )

    # Campo Marca
    marca = forms.ChoiceField(
        choices=BRAND_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        label='Marca'
    )
    
    # Campo Tipo (Condición)
    condition = forms.ChoiceField(
        choices=CONDITION_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Condición'
    )
    
    # Campos Rango de Precio (Min/Max)
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
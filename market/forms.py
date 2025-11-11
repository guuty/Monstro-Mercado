from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from market.models import Product  


# ========== FORMULARIO DE REGISTRO CON ALLAUTH ==========
class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrega las clases de Bootstrap y placeholders a todos los campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Agrega placeholders específicos si los campos existen
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({
                'placeholder': 'tu@email.com'
            })
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({
                'placeholder': 'usuario123',
                'autocomplete': 'username'
            })
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'placeholder': '••••••••',
                'autocomplete': 'new-password'
            })
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'placeholder': '••••••••',
                'autocomplete': 'new-password'
            })


# ========== FORMULARIO DE REGISTRO MANUAL (si no usas allauth) ==========
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Requerido. Ingresá una dirección de email válida.',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'usuario123'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••'
        })


# ========== FORMULARIO DE PRODUCTOS ==========
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'marca', 'price', 'stock', 'image', 'active'] 
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre o título del producto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe el producto en detalle'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Sony, Samsung, Genérica'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1',
                'min': '0'
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
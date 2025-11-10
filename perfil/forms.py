from django import forms
from django.contrib.auth.models import User  # <--- ESTO ES LO QUE FALTABA O SE PERDIÓ
from .models import Profile # Asegúrate de que tu modelo Profile esté aquí

# Formulario para campos del modelo User (nombre, apellido)
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', max_length=150, required=True, 
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Apellido', max_length=150, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User # Aquí se necesita la clase User importada
        fields = ['first_name', 'last_name']
        
# Formulario para campos del modelo Profile (bio, avatar, etc.)
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(label='Biografía', required=False, 
                          widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    # Agrega el resto de tus campos de Profile si los tienes

    class Meta:
        model = Profile
        fields = ['bio', 'website', 'avatar'] # O los campos que tengas
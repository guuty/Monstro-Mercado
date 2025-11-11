from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# --- 🎯 CORRECCIÓN CLAVE ---
# Debemos importar los nombres de las clases que definiste en forms.py
from .forms import UserUpdateForm, ProfileUpdateForm 
# ---------------------------


@login_required
def edit_profile(request):
    # Ya no usamos 'profile = request.user.profile' directamente en el GET
    # Lo manejamos a través de la instancia en los formularios.

    if request.method == 'POST':
        # 1. Instanciar el formulario del Usuario (first_name, last_name)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        # 2. Instanciar el formulario del Perfil (bio, avatar, etc.)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        # Validar ambos formularios
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            # Usar Django Messages para notificar al usuario (opcional pero recomendado)
            messages.success(request, '¡Tu perfil ha sido actualizado correctamente, incluyendo tu nombre!')
            
            # Redirigir a la vista de perfil principal
            return redirect('profile') 
        else:
            # Si hay errores de validación, los formularios (con errores) se pasarán al contexto
            messages.error(request, 'Hubo un error al guardar los datos. Revisa los campos.')
            
    else:
        # Petición GET: Instanciar formularios con los datos actuales
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        # Ahora pasamos AMBOS formularios al template profile_edit.html
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, "perfil/profile_edit.html", context)


@login_required
def profile_view(request):
    # Esta vista está bien, solo usa el perfil para renderizar la plantilla.
    return render(request, "perfil/profile.html", {"profile": request.user.profile})
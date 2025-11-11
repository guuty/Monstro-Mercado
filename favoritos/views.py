from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator

from productos.models import Producto  # ✅ CORREGIDO
from .models import Favorite


@login_required
@require_POST
def toggle_favorite(request, pk):
    """
    Alterna el estado de favorito de un producto.
    Si existe, lo elimina. Si no existe, lo crea.
    """
    # 1. Obtener el producto o devolver 404
    product = get_object_or_404(Producto, pk=pk)  # ✅ CORREGIDO
    user = request.user
    
    # 2. Buscar si ya existe el favorito
    favorite, created = Favorite.objects.get_or_create(
        user=user, 
        product=product
    )

    is_favorited = False
    
    if created:
        # 3. Si se acaba de crear, es un favorito nuevo
        is_favorited = True
    else:
        # 4. Si ya existía, lo eliminamos (toggle/alternar)
        favorite.delete()
        is_favorited = False

    # 5. Devolver la respuesta JSON
    return JsonResponse({
        'status': 'success', 
        'is_favorited': is_favorited
    })


@method_decorator(login_required, name='dispatch')
class FavoriteListView(ListView):
    """
    Muestra la lista de productos favoritos del usuario.
    """
    model = Favorite
    template_name = 'favoritos/favorite_list.html'
    context_object_name = 'favoritos'  # ✅ Nombre más claro

    def get_queryset(self):
        # Filtra solo los favoritos del usuario actual
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favoritos_count'] = self.get_queryset().count()
        return context
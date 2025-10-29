from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from market.models import Product  
from .models import Favorite         

@login_required
@require_POST
def toggle_favorite(request, pk):
    # 1. Obtener el producto o devolver 404
    product = get_object_or_404(Product, pk=pk)
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
    return JsonResponse({'status': 'success', 'is_favorited': is_favorited})

# Vista para listar (para que puedas comprobar la lista)
from django.views.generic import ListView
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class FavoriteListView(ListView):
    model = Favorite
    template_name = 'favoritos/favorite_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        # Filtra solo los favoritos del usuario actual
        return Favorite.objects.filter(user=self.request.user).select_related('product')
    

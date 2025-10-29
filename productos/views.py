from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from favoritos.models import Favorite
from django.views.generic import DetailView

from market.models import Product 
from .forms import ProductForm, ProductFilterForm 


# Vista para listar productos (CON FILTROS INTEGRADOS)
def lista_productos(request):
    # 1. Inicializa la consulta base
    productos = Product.objects.all().order_by('-created_at') # Ordena por más reciente por defecto
    
    # 2. Inicializa el formulario de filtros con los datos de la URL (request.GET)
    form = ProductFilterForm(request.GET)
    
    # --- APLICACIÓN DE FILTROS ---
    if form.is_valid():
        # Obtiene los datos limpios del formulario
        category = form.cleaned_data.get('category')
        marca = form.cleaned_data.get('marca')
        condition = form.cleaned_data.get('condition')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        
        # Filtro por Categoría (si no es el valor por defecto/vacío)
        if category:
            productos = productos.filter(category=category)
            
        # Filtro por Marca (si no es el valor por defecto/vacío)
        if marca:
            productos = productos.filter(marca=marca)
            
        # Filtro por Condición (Tipo)
        if condition:
            productos = productos.filter(condition=condition)
            
        # Filtro por Rango de Precio
        if price_min is not None:
            productos = productos.filter(price__gte=price_min) # greater than or equal
            
        if price_max is not None:
            productos = productos.filter(price__lte=price_max) # less than or equal
    # -----------------------------
    
    # 3. LÓGICA DE FAVORITOS (existente)
    if request.user.is_authenticated:
        favorited_subquery = Favorite.objects.filter(
            user=request.user, 
            product=OuterRef('pk')
        )
        productos = productos.annotate(
            is_favorited=Exists(favorited_subquery)
        )
    
    # DEBUG (opcional, si lo quieres mantener)
    print("=" * 50)
    print(f"Cantidad de productos: {productos.count()}")
    for p in productos:
        is_fav = getattr(p, 'is_favorited', False)
        print(f"- {p.title}: ${p.price} | ¿Favorito? {is_fav}")
    print("=" * 50)
    
    # Pasamos los productos filtrados, el formulario de filtros y la cuenta total
    context = {
        'products': productos,
        'filter_form': form,             
        'product_count': productos.count(), 
    }
    
    
    return render(request, 'productos/productos_list.html', context)


# Vista para crear un producto (EXISTENTE)
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) 
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user 
            product.save()
            return redirect('productos:product_list') 
    else:
        form = ProductForm()
    
    return render(request, 'productos/product_form.html', {'form': form})


# Class-Based View para detalles del producto (EXISTENTE)
class ProductDetailView(DetailView):
    model = Product
    template_name = 'productos/product_detail.html' 
    context_object_name = 'product' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(
                user=self.request.user, 
                product=self.object 
            ).exists()
        else:
            context['is_favorited'] = False
        return context
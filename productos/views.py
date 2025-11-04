from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Exists, OuterRef
from django.views.generic import DetailView

from productos.models import Producto, Carrito, ItemCarrito
from .forms import ProductForm, ProductFilterForm

# Intenta importar Favorite, si falla usa None
try:
    from productos.models import Favorite
except ImportError:
    try:
        from favoritos.models import Favorite
    except ImportError:
        Favorite = None
# Vista para listar productos (CON FILTROS INTEGRADOS)
def lista_productos(request):
    # 1. Inicializa la consulta base
    productos = Producto.objects.all().order_by('creado')
    
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
            productos = productos.filter(precio__gte=price_min)
            
        if price_max is not None:
            productos = productos.filter(precio__lte=price_max)
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
    
    print("=" * 50)
    print(f"Cantidad de productos: {productos.count()}")
    for producto in productos:
        is_fav = getattr(producto, 'is_favorited', False)
        print(f"- {producto.nombre}: ${producto.precio} | ¿Favorito? {is_fav}")
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


# Class-Based View para detalles del producto (CORREGIDA)
class ProductDetailView(DetailView):
    model = Producto
    template_name = 'productos/product_detail.html' 
    context_object_name = 'producto'  # ← Cambia a 'producto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(
                user=self.request.user,
                product=self.get_object()  # ← Usa self.get_object() en lugar de self.object
            ).exists()
        else:
            context['is_favorited'] = False
        
        return context


# VISTAS DEL CARRITO
from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    context = {
        'carrito': carrito,
        'items': carrito.items.all()
    }
    return render(request, 'productos/ver_carrito.html', context)

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    if producto.stock <= 0:
        messages.error(request, 'Producto sin stock')
        return redirect('productos:product_detail', pk=producto_id)
    
    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto
    )
    
    if not created:
        if item.cantidad < producto.stock:
            item.cantidad += 1
            item.save()
            messages.success(request, f'Cantidad actualizada: {item.cantidad}x {producto.nombre}')
        else:
            messages.warning(request, 'No hay más stock disponible')
    else:
        messages.success(request, f'{producto.nombre} agregado al carrito')
    
    return redirect('productos:ver_carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    nombre_producto = item.producto.nombre
    item.delete()
    messages.success(request, f'{nombre_producto} eliminado del carrito')
    return redirect('productos:ver_carrito')

@login_required
def vaciar_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    carrito.items.all().delete()
    messages.success(request, 'Carrito vaciado')
    return redirect('productos:ver_carrito')
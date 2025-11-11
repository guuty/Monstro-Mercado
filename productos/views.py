from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Exists, OuterRef, Q
from django.views.generic import DetailView

from productos.models import Producto, Carrito, ItemCarrito, Pedido, ItemPedido
from .forms import ProductForm, ProductFilterForm

import requests
from django.http import JsonResponse
import mercadopago
from django.conf import settings 

# Importar Favorite desde favoritos
try:
    from favoritos.models import Favorite
except ImportError:
    Favorite = None


# ========== VISTA LISTA DE PRODUCTOS ==========
def lista_productos(request):
    # 1. Inicializa la consulta base
    productos = Producto.objects.all().order_by('-creado')
    
    # ========== BÚSQUEDA POR TEXTO ==========
    search_query = request.GET.get('q', '').strip()
    if search_query:
        productos = productos.filter(
            Q(nombre__icontains=search_query) |
            Q(descripcion__icontains=search_query) |
            Q(marca__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # 2. Inicializa el formulario de filtros
    form = ProductFilterForm(request.GET)
    
    # --- APLICACIÓN DE FILTROS ---
    if form.is_valid():
        category = form.cleaned_data.get('category')
        marca = form.cleaned_data.get('marca')
        condition = form.cleaned_data.get('condition')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        
        if category:
            productos = productos.filter(category=category)
        if marca:
            productos = productos.filter(marca=marca)
        if condition:
            productos = productos.filter(condition=condition)
        if price_min is not None:
            productos = productos.filter(precio__gte=price_min)
        if price_max is not None:
            productos = productos.filter(precio__lte=price_max)
    
    # Ordenar
    orderby = request.GET.get('orderby')
    if orderby:
        productos = productos.order_by(orderby)
    
    # 3. LÓGICA DE FAVORITOS
    if request.user.is_authenticated and Favorite:
        favorited_subquery = Favorite.objects.filter(
            user=request.user, 
            product=OuterRef('pk')
        )
        productos = productos.annotate(
            is_favorited=Exists(favorited_subquery)
        )
    
    context = {
        'products': productos,
        'filter_form': form,
        'product_count': productos.count(),
        'search_query': search_query,
    }
    
    return render(request, 'productos/productos_list.html', context)


# ========== CREAR PRODUCTO ==========
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) 
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user 
            product.save()
            messages.success(request, 'Producto creado exitosamente')
            return redirect('productos:product_list') 
    else:
        form = ProductForm()
    
    return render(request, 'productos/product_form.html', {'form': form})


# ========== DETALLE DEL PRODUCTO ==========
class ProductDetailView(DetailView):
    model = Producto
    template_name = 'productos/product_detail.html' 
    context_object_name = 'producto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated and Favorite:
            context['is_favorited'] = Favorite.objects.filter(
                user=self.request.user,
                product=self.get_object()
            ).exists()
        else:
            context['is_favorited'] = False
        
        return context


# ========== VISTAS DEL CARRITO ==========
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


# ========== MERCADO PAGO ==========
@login_required
def create_preference_cart(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    if not carrito.items.exists():
        return JsonResponse({"error": "El carrito está vacío"}, status=400)

    items = []
    for item in carrito.items.all():
        items.append({
            "title": item.producto.nombre,
            "quantity": item.cantidad,
            "unit_price": float(item.producto.precio),
            "currency_id": "ARS" 
        })
    
    url = "https://api.mercadopago.com/checkout/preferences"

    headers = {
        "Authorization": f"Bearer {settings.MERCADOPAGO_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "items": items,
        "back_urls": {
            "success": settings.SITE_URL + "/products/pago-exitoso/",
            "failure": settings.SITE_URL + "/products/pago-fallido/",
            "pending": settings.SITE_URL + "/products/pago-pendiente/",
        },
        "auto_return": "approved"
    }

    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 201:
        data = response.json()
        preference_id = data.get("id", "ID no encontrada")
        print("✅ PREFERENCIA CREADA:", preference_id)
        return JsonResponse({"init_point": data.get("init_point")})
    else:
        try:
            error_data = response.json()
        except requests.exceptions.JSONDecodeError:
            error_data = {"message": response.text or "Error en MP"}
        
        print(f"🛑 ERROR MP: {response.status_code}", error_data)
        return JsonResponse({
            "error": "No se pudo generar el link de pago",
            "detail": error_data.get("message", "Error desconocido")
        }, status=response.status_code if response.status_code >= 400 else 400)


# ========== PAGO EXITOSO (CREA EL PEDIDO) ==========
@login_required
def pago_exitoso(request):
    """
    Vista que se muestra después de un pago exitoso.
    Crea el pedido y vacía el carrito.
    """
    # Obtener datos de Mercado Pago
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    preference_id = request.GET.get('preference_id')
    
    # Obtener el carrito
    try:
        carrito = Carrito.objects.get(usuario=request.user)
    except Carrito.DoesNotExist:
        messages.error(request, 'No se encontró un carrito')
        return redirect('home')
    
    # Verificar que el carrito no esté vacío
    if not carrito.items.exists():
        messages.warning(request, 'El carrito está vacío')
        return redirect('productos:product_list')
    
    # Crear el pedido
    pedido = Pedido.objects.create(
        usuario=request.user,
        nombre_completo=f"{request.user.first_name} {request.user.last_name}" or request.user.username,
        email=request.user.email,
        telefono="",
        direccion="Por definir",
        subtotal=carrito.calcular_total(),
        descuento=0,
        total=carrito.calcular_total(),
        preference_id=preference_id,
        payment_id=payment_id,
        estado='pagado' if status == 'approved' else 'pendiente'
    )
    
    # Crear los items del pedido
    for item in carrito.items.all():
        ItemPedido.objects.create(
            pedido=pedido,
            producto=item.producto,
            nombre_producto=item.producto.nombre,
            precio_unitario=item.producto.precio,
            cantidad=item.cantidad,
            subtotal=item.producto.precio * item.cantidad
        )
        
        # Descontar del stock
        if item.producto.stock >= item.cantidad:
            item.producto.stock -= item.cantidad
            item.producto.save()
    
    # Vaciar el carrito
    carrito.items.all().delete()
    
    messages.success(request, f'¡Compra exitosa! Tu número de pedido es: {pedido.numero_pedido}')
    
    # Redirigir al ticket
    return redirect('productos:ver_ticket', pedido_id=pedido.id)


# ========== VER TICKET ==========
@login_required
def ver_ticket(request, pedido_id):
    """
    Muestra el ticket del pedido para imprimir.
    """
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    
    context = {
        'pedido': pedido,
    }
    
    return render(request, 'productos/ticket.html', context)


# ========== MIS PEDIDOS ==========
@login_required
def mis_pedidos(request):
    """
    Lista todos los pedidos del usuario.
    """
    pedidos = Pedido.objects.filter(usuario=request.user)
    
    context = {
        'pedidos': pedidos,
    }
    
    return render(request, 'productos/mis_pedidos.html', context)


# ========== VISTAS DE PAGO (FALLIDO/PENDIENTE) ==========
@login_required
def pago_fallido(request):
    messages.error(request, 'El pago no pudo ser procesado. Intentá nuevamente.')
    return redirect('productos:ver_carrito')


@login_required
def pago_pendiente(request):
    messages.warning(request, 'El pago está pendiente de confirmación.')
    return redirect('productos:ver_carrito')
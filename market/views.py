from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .forms import SignUpForm, ProductForm 
from .models import Product


def product_list(request):
    # Obtener todos los productos
    products = Product.objects.filter(active=True).order_by('-created_at')
    
    # ========== BÚSQUEDA (texto o voz) ==========
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(marca__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # Filtrar por categoría
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    
    # Filtrar por marca
    marca = request.GET.get('marca')
    if marca:
        products = products.filter(marca__icontains=marca)
    
    # Filtrar por condición (nuevo/usado)
    condition = request.GET.get('condition')
    if condition:
        products = products.filter(condition=condition)
    
    # Filtrar por rango de precio
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    
    # Ordenar
    orderby = request.GET.get('orderby', '-created_at')
    products = products.order_by(orderby)
    
    context = {
        'products': products,
        'product_count': products.count(),
        'search_query': search_query,
    }
    
    return render(request, "market/product_list.html", context)


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, "Producto creado exitosamente")
            return redirect("productos:product-list")
    else:
        form = ProductForm()
    return render(request, "market/product_form.html", {"form": form})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado exitosamente")
            return redirect("productos:product-list")
    else:
        form = ProductForm(instance=product)
    return render(request, "market/product_form.html", {"form": form})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if product.seller != request.user:
        messages.error(request, "No podés eliminar este producto")
        return redirect("productos:product-list")
    
    if request.method == "POST":
        product.delete()
        messages.success(request, "Producto eliminado")
        return redirect("productos:product-list")
    
    return render(request, "market/product_confirm_delete.html", {"product": product})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('productos:product-list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# ========== VISTA PARA CARRITO (NUEVA) ==========
@login_required
def carrito_view(request):
    # Por ahora simple, después agregamos más funcionalidad
    context = {
        'page_title': 'Mi Carrito'
    }
    return render(request, "market/carrito.html", context)
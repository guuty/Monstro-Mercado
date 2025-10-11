from django.shortcuts import render
from market.models import Product  # ← Cambiar esto

def lista_productos(request):
    productos = Product.objects.all()  # ← Usar Product
    print("=" * 50)
    print(f"Cantidad de productos: {productos.count()}")
    print(f"Productos: {productos}")
    for p in productos:
        print(f"- {p.title}: ${p.price}")
    print("=" * 50)
    return render(request, 'productos/productos_list.html', {'products': productos})
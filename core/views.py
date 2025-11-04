from django.shortcuts import render
from productos.models import Producto

def home(request):
    products = Producto.objects.all().order_by('-creado')[:8]
    return render(request, "home.html", {"products": products})
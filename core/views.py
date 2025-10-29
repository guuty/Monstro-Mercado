from django.shortcuts import render
from market.models import Product

def home(request):
    products = Product.objects.all().order_by('-created_at')[:8]
    #products = Product.objects.filter(active=True).order_by("-created_at")[:6]  # últimos 6
    return render(request, "home.html", {"products": products})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, "market/product_list.html",{"products ": products})

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect("product-list")
    else:
        form = ProductForm()
    return render(request, "market/product_form.html", {"form": form})

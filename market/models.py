from django.conf import settings
from django.db import models

class Product(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="products"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    marca = models.CharField(max_length=100, blank=True, default="Genérico")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    CONDITION_CHOICES = [
        ('new', 'Nuevo'),
        ('used', 'Usado'),
    ]
    condition = models.CharField(
        max_length=4,
        choices=CONDITION_CHOICES,
        default='new'
    )
    
    # Campo para Categoría - ACTUALIZADO PARA SUPERMERCADO
    CATEGORY_CHOICES = [
        ('bebidas', 'Bebidas'),
        ('almacen', 'Almacén'),
        ('frescos', 'Frescos'),
        ('lacteos', 'Lácteos'),
        ('carnes', 'Carnes y Pescados'),
        ('verduras', 'Frutas y Verduras'),
        ('panaderia', 'Panadería'),
        ('limpieza', 'Limpieza'),
        ('perfumeria', 'Perfumería'),
        ('congelados', 'Congelados'),
        ('snacks', 'Snacks y Golosinas'),
        ('pastas', 'Pastas'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='almacen'
    )
    
    def __str__(self):
        return self.title

    def is_available(self):
        return self.active and self.stock > 0
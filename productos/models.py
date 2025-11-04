from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    # Categorías de supermercado
    CATEGORY_CHOICES = [
        ('almacen', 'Almacén'),
        ('bebidas', 'Bebidas'),
        ('lacteos', 'Lácteos y Huevos'),
        ('carnes', 'Carnes y Pescados'),
        ('frutas', 'Frutas y Verduras'),
        ('panaderia', 'Panadería'),
        ('limpieza', 'Limpieza'),
        ('higiene', 'Higiene Personal'),
        ('congelados', 'Congelados'),
        ('snacks', 'Snacks y Golosinas'),
        ('desayuno', 'Desayuno y Cereales'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'Nuevo'),
        ('used', 'Usado'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    
    # CAMPOS NUEVOS
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='almacen', verbose_name='Categoría')
    marca = models.CharField(max_length=100, blank=True, verbose_name='Marca')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='new', verbose_name='Condición')
    
    # CAMPO SELLER AGREGADO
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos', verbose_name='Vendedor', null=True, blank=True, default=1)
    
    creado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Productos"
    
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
    def total(self):
        return sum(item.subtotal() for item in self.items.all())
    
    def cantidad_items(self):
        return sum(item.cantidad for item in self.items.all())
    
    class Meta:
        verbose_name_plural = "Carritos"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    agregado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"
    
    def subtotal(self):
        return self.producto.precio * self.cantidad
    
    class Meta:
        verbose_name_plural = "Items del Carrito"
        unique_together = ('carrito', 'producto')

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Se llama 'product'
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')
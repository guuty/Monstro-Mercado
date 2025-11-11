from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid

# ========== MODELO PRODUCTO (DEBE IR PRIMERO) ==========
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


# ========== MODELO CARRITO ==========
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
    def calcular_total(self):
        """Calcula el total del carrito"""
        return sum(item.subtotal() for item in self.items.all())
    
    def cantidad_items(self):
        """Cuenta la cantidad total de items"""
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


# ========== MODELOS DE PEDIDOS ==========
class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    numero_pedido = models.CharField(max_length=20, unique=True, editable=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    # Datos de contacto (guardados en el momento de la compra)
    nombre_completo = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField()
    
    # Totales
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Mercado Pago
    preference_id = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
    
    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            # Generar número de pedido único
            self.numero_pedido = f"PED-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.usuario.username}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    
    # Guardamos los datos del producto en el momento de la compra
    nombre_producto = models.CharField(max_length=200)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        # Calcular subtotal automáticamente
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.cantidad}x {self.nombre_producto}"
    
    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Items de Pedidos'
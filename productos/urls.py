from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    # Productos
    path('lista/', views.lista_productos, name='product_list'),
    path('nuevo/', views.create_product, name='product_create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    
    # Mercado Pago
    path('crear-preferencia/', views.create_preference_cart, name='crear_preferencia'),
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago-pendiente/', views.pago_pendiente, name='pago_pendiente'),
    
    # Pedidos y Tickets
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('ticket/<int:pedido_id>/', views.ver_ticket, name='ver_ticket'),
]
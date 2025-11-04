from django.urls import path
from . import views
from .views import ProductDetailView

app_name = 'productos'

urlpatterns = [
    # Productos
    path('', views.lista_productos, name='product_list'),
    path('crear/', views.create_product, name='product_create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
]
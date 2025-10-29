from django.urls import path
from . import views
from .views import ProductDetailView
from .views import lista_productos, create_product

app_name = 'productos'

urlpatterns = [
    path('', views.lista_productos, name='product_list'),
    path('crear/', views.create_product, name='product-create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
]
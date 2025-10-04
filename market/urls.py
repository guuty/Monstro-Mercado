from django.urls import path
from .views import product_list , product_create

urlpatterns = [
    path("lista/", product_list, name="product-list"),
    path("nuevo/", product_create, name="product-create"),
]

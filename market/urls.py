from django.urls import path
from . import views

urlpatterns = [
    path("lista/", views.product_list, name="product-list"),
    path("nuevo/", views.product_create, name="product-create"),
    path("editar/<int:pk>/", views.product_edit, name="product-edit"),
    path("eliminar/<int:pk>/", views.product_delete, name="product-delete"),
    path('signup/', views.signup, name='account_signup'),
]
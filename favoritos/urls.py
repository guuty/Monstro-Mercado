from django.urls import path
from . import views


app_name = 'favoritos'

urlpatterns = [
    
     path('', views.FavoriteListView.as_view(), name='list'),
     path('toggle/<int:pk>/', views.toggle_favorite, name='toggle'),
    
]
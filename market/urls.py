from django.contrib import admin
from django.urls import path, include

app_name = "market"

urlpatterns = [
    path("admin/", admin.site.urls),
    #path("products/", include("market.urls")),
]
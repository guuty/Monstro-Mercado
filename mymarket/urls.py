from django.contrib import admin
from django.urls import path, include
from core.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("accounts/", include("allauth.urls")),  # allauth
    path("products/", include("market.urls")),  # productos
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
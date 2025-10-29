from django.conf import settings
from django.db import models
# Ajusta la importación de Product según dónde esté (ej: from productos.models import Product)
from market.models import Product  # Asumiendo que Product está en market.models

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Esto asegura que un usuario solo pueda marcar el mismo producto una vez
        unique_together = ('user', 'product')
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str__(self):
        return f"{self.user.username} likes {self.product.title}"
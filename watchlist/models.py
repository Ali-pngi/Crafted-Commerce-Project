from django.db import models
from django.conf import settings
from products.models import Product

class WatchlistItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='watchlist_items'  
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='watchlist_items_product'  
    )

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} - {self.product.title}'

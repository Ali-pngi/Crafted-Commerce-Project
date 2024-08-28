from django.db import models

# Create your models here.

class Offer(models.Model):
    price = models.IntegerField
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        'products.Product', 
        on_delete=models.CASCADE,
        related_name='offers'
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        on_delete=models.CASCADE,
        related_name='offers_created'
    )
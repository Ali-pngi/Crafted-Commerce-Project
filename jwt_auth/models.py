from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Product
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.TextField(unique=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(Product, related_name='watched_by')

    def __str__(self):
        return self.username

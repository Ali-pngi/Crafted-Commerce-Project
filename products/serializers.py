# products/serializers.py

from rest_framework import serializers
from .models import Product, ProductImage
from watchlist.models import WatchlistItem

from django.contrib.auth import get_user_model

User = get_user_model()

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'uploaded_at']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'images', 'created_at', 'updated_at']

class WatchlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = WatchlistItem
        fields = ['id', 'user', 'product']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

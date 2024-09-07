# products/serializers.py

from rest_framework import serializers
from .models import Product, ProductImage
from watchlist.models import WatchlistItem
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'uploaded_at']

    def get_image_url(self, obj):
        
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    # image = serializers.URLField(write_only=True, required=False)
    
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

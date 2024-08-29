from rest_framework import serializers
from .models import Product, ProductImage, Watchlist

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'uploaded_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        return obj.image.url if obj.image else None

class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'owner', 'title', 'description', 'price', 'main_image', 'images', 'created_at', 'updated_at']

    def get_main_image(self, obj):
        main_image = obj.images.first()
        request = self.context.get('request')
        return main_image.image.url if main_image and main_image.image else None

class ProductPreviewSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'main_image']

    def get_main_image(self, obj):
        main_image = obj.images.first()
        return main_image.image.url if main_image and main_image.image else None

class WatchlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  

    class Meta:
        model = Watchlist
        fields = ['id', 'user', 'product', 'added_at']

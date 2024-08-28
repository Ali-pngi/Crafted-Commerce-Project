

from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'price')
    inlines = [ProductImageInline]  

admin.site.register(Product, ProductAdmin)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),  # Include your products app URLs
    path('api/auth/', include('jwt_auth.urls')), 
    path('api/offers/', include('offers.urls')),
]

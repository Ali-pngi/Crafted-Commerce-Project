from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),  
    path('api/auth/', include('jwt_auth.urls')),
    path('api/watchlist/', include('watchlist.urls')),
    path('api/', include('jwt_auth.urls')),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.WatchlistView.as_view(), name='watchlist'),  
    path('<int:product_id>/', views.ToggleWatchlistView.as_view(), name='toggle_watchlist'),  
]

from django.urls import path
from .views import SignUpView, SignInView, AddToWatchlistView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('watchlist/<int:pk>/', AddToWatchlistView.as_view(), name='add_to_watchlist'),
]

# jwt_auth/urls.py

from django.urls import path
from .views import SignUpView, SignInView, check_username, check_email

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('check-username/', check_username, name='check-username'),
    path('check-email/', check_email, name='check-email'),
]

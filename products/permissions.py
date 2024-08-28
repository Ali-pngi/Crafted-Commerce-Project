# products/permissions.py

from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit products.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS include GET, HEAD, and OPTIONS requests.
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_staff

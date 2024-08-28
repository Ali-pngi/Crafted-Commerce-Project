# offers/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Offer
from .serializers import OfferSerializer
from jwt_auth.permissions import IsAdminOrReadOnly  

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrReadOnly]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


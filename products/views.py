from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, ProductImage
from watchlist.models import WatchlistItem
from .serializers import ProductSerializer, WatchlistItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_to_watchlist(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        watchlist_item, created = WatchlistItem.objects.get_or_create(user=request.user, product=product)

        if created:
            return Response({'status': 'Product added to watchlist'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Product already in watchlist'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def remove_from_watchlist(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        try:
            watchlist_item = WatchlistItem.objects.get(user=request.user, product=product)
            watchlist_item.delete()
            return Response({'status': 'Product removed from watchlist'}, status=status.HTTP_204_NO_CONTENT)
        except WatchlistItem.DoesNotExist:
            return Response({'error': 'Product not in watchlist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def watchlist(self, request):
        watchlist_items = WatchlistItem.objects.filter(user=request.user)
        serializer = WatchlistItemSerializer(watchlist_items, many=True)
        return Response(serializer.data)


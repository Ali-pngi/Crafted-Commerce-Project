from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Watchlist, Product
from .serializers import WatchlistSerializer, ProductSerializer, ProductPreviewSerializer

class WatchlistViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        watchlist = Watchlist.objects.filter(user=user)
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            watchlist_item = Watchlist.objects.get(pk=pk, user=request.user)
            watchlist_item.delete()
            return Response(status=204)
        except Watchlist.DoesNotExist:
            return Response(status=404)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Adjust as needed

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductPreviewSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        serializer.save()


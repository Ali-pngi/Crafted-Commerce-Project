# watchlist/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WatchlistItem
from products.models import Product

class WatchlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        watchlist_items = WatchlistItem.objects.filter(user=request.user)
        serialized_data = [
            {"product_id": item.product.id, "product_title": item.product.title}
            for item in watchlist_items
        ]
        return Response(serialized_data, status=status.HTTP_200_OK)

class ToggleWatchlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        
        watchlist_item, created = WatchlistItem.objects.get_or_create(user=request.user, product=product)

        if not created:
            watchlist_item.delete()
            return Response({"message": "Removed from watchlist"}, status=status.HTTP_200_OK)
        
        
        return Response({"message": "Added to watchlist"}, status=status.HTTP_201_CREATED)

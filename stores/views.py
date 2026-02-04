from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Inventory

class StoreInventoryAPIView(APIView):
    def get(self, request, store_id):
        inventories = (
            Inventory.objects
            .filter(store_id=store_id)
            .select_related("product__category")
            .order_by("product__title")
        )

        return Response([
            {
                "product": i.product.title,
                "price": i.product.price,
                "category": i.product.category.name,
                "quantity": i.quantity
            }
            for i in inventories
        ])

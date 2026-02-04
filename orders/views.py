from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

from .models import Order, OrderItem
from stores.models import Inventory

class OrderCreateAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        store_id = request.data.get("store_id")
        items = request.data.get("items", [])

        order = Order.objects.create(
            store_id=store_id,
            status=Order.PENDING
        )

        inventories = Inventory.objects.select_for_update().filter(store_id=store_id)
        inventory_map = {i.product_id: i for i in inventories}

        for item in items:
            inv = inventory_map.get(item["product_id"])
            if not inv or inv.quantity < item["quantity_requested"]:
                order.status = Order.REJECTED
                order.save()
                return Response({"status": "REJECTED"}, status=400)

        for item in items:
            inv = inventory_map[item["product_id"]]
            inv.quantity -= item["quantity_requested"]
            inv.save()

            OrderItem.objects.create(
                order=order,
                product_id=item["product_id"],
                quantity_requested=item["quantity_requested"]
            )

        order.status = Order.CONFIRMED
        order.save()

        return Response({"status": "CONFIRMED", "order_id": order.id})

class StoreOrderListAPIView(APIView):
    def get(self, request, store_id):
        orders = (
            Order.objects
            .filter(store_id=store_id)
            .annotate(total_items=Sum("items__quantity_requested"))
            .order_by("-created_at")
        )

        return Response([
            {
                "order_id": o.id,
                "status": o.status,
                "created_at": o.created_at,
                "total_items": o.total_items or 0
            }
            for o in orders
        ])
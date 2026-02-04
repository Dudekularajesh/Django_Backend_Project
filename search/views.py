from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from stores.models import Inventory

class ProductSearchAPIView(APIView):
    def get(self, request):
        q = request.GET.get("q", "")
        store_id = request.GET.get("store_id")

        qs = Product.objects.select_related("category")

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )

        data = []
        for p in qs[:50]:
            item = {
                "title": p.title,
                "price": p.price,
                "category": p.category.name
            }
            if store_id:
                inv = Inventory.objects.filter(store_id=store_id, product=p).first()
                item["quantity"] = inv.quantity if inv else 0
            data.append(item)

        return Response(data)

class ProductSuggestAPIView(APIView):
    def get(self, request):
        q = request.GET.get("q", "")

        if len(q) < 3:
            return Response([])

        products = Product.objects.filter(title__istartswith=q)[:10]
        return Response([p.title for p in products])
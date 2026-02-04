from django.db import models
from stores.models import Store
from products.models import Product

class Order(models.Model):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (REJECTED, "Rejected"),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField()

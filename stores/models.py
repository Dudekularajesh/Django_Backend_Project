from django.db import models
from products.models import Product

class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="inventories")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("store", "product")

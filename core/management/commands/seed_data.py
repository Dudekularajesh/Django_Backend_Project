from django.core.management.base import BaseCommand
from faker import Faker
from products.models import Category, Product
from stores.models import Store, Inventory
import random

class Command(BaseCommand):
    help = "Seed database with dummy data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        categories = [
            Category.objects.create(name=fake.word())
            for _ in range(10)
        ]

        products = [
            Product.objects.create(
                title=fake.sentence(nb_words=3),
                price=random.randint(50, 500),
                category=random.choice(categories)
            )
            for _ in range(1000)
        ]

        stores = [
            Store.objects.create(
                name=fake.company(),
                location=fake.city()
            )
            for _ in range(20)
        ]

        for store in stores:
            for product in random.sample(products, 300):
                Inventory.objects.create(
                    store=store,
                    product=product,
                    quantity=random.randint(1, 100)
                )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully"))

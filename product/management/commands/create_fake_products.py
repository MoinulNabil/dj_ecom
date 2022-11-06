import requests

from django.core.management.base import BaseCommand

from product.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = 'https://fakestoreapi.com/products'
        products = requests.get(url).json()

        for product in products:
            category = Category.objects.filter(
                title__iexact=product['category']
            )

            if category.exists():
                category = category.first()
            else:
                category = Category.objects.create(
                    title=product['category'],
                    featured=True
                )
            
            Product.objects.create(
                category=category,
                title=product['title'],
                price=product['price'],
                thumbnail=product['image'],
                description=product['description'],
                stock=10
            )

        print("products created")

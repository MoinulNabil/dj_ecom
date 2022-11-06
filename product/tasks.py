from django.core.cache import cache

from celery import shared_task

from .models import Product

@shared_task
def reset_product_cache(key):
    cache.delete(key)
    cache.set(key, Product.objects.all())
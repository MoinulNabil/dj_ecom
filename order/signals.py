from datetime import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from .models import Order


@receiver(post_save, sender=Order)
def generate_invoice_while_order_created(instance, created, *args, **kwargs):
    if created:
        instance.invoice_id = str(datetime.strftime(timezone.now(), '%Y-%m-%d')).replace('-', '') + str(instance.id)
        instance.save()

from decimal import Decimal

from django.db import models
from django.conf import settings

from django_countries.fields import CountryField

from product.models import Product


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='product_order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2
    )
    discount_in_percentage = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'OrderItems'
        ordering = ['-created_date']

    def __str__(self) -> str:
        return self.product.title

    @property
    def get_total(self):
        return (self.price - (self.price * Decimal(self.discount_in_percentage / 100))) * self.quantity


class Order(models.Model):
    STATUS = ("Received", "On the way", "Delivered")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    order_items = models.ManyToManyField(OrderItem)
    first_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        max_length=150
    )
    phone_number = models.CharField(
        max_length=11
    )
    transaction_id = models.CharField(
        max_length=60,
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=100
    )
    country = CountryField()
    zip_code = models.CharField(
        max_length=10
    )
    address = models.CharField(
        max_length=500
    )
    invoice_id = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=15,
        choices=list(zip(STATUS, STATUS)),
        default="Received"
    )
    total = models.DecimalField(
        max_digits=21,
        decimal_places=2
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "orders"
        ordering = ['-created_date']

    def __str__(self) -> str:
        return self.first_name + ' '+ self.last_name

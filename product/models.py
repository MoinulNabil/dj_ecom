from decimal import Decimal
from django.db import models

from core.utilities import generate_unique_slug


class Category(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        null=True,
        blank=True
    )
    featured = models.BooleanField(default=False)
    logo = models.URLField(
        null=True,
        blank=True
    )
    description = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        default="No description available"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def get_logo(self):
        if self.logo:
            return self.logo
        else:
            return '/static/img/default-category-logo.jpg'

    def get_products(self):
        return self.category_products.all()


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='category_products',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=250
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        null=True,
        blank=True
    )
    thumbnail = models.URLField()
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2
    )
    discount_in_percentage = models.PositiveIntegerField(default=0)
    description = models.TextField(
        null=True,
        blank=True,
        default='No description available'
    )
    featured = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'products'
        ordering = ['-created_date']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    @property
    def get_images(self):
        return self.productimages_set.all()

    @property
    def get_variations(self):
        return self.product_variations.all()

    @property
    def get_price(self):
        if self.discount_in_percentage > 0:
            return self.price - (self.price * Decimal(self.discount_in_percentage / 100))
        else:
            return self.price

    @property
    def get_similar(self):
        return self.category.get_products().exclude(pk=self.pk)


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='product_images',
        on_delete=models.CASCADE
    )
    image_url = models.URLField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'productimages'
        ordering = ['-created_date']

    def __str__(self) -> str:
        return self.product.title


from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductImages
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'featured', ]


admin.site.register(Category, CategoryAdmin)


class ProductImagesTabular(admin.TabularInline):
    model = ProductImages
    extra = 5


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesTabular, ]
    list_display = ['__str__', 'featured', 'price', 'discount_in_percentage', ]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages)

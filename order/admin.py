from django.contrib import admin


from .models import (
    OrderItem,
    Order
)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'price',
        'discount_in_percentage',
        'quantity',
        'created_date'
    ]
    list_filter = [
        'created_date'
    ]
    list_per_page = 20


admin.site.register(OrderItem, OrderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'phone_number',
        'first_name',
        'last_name',
        'total',
        'status',
        'created_date'
    ]
    list_filter = [
        'status',
        'created_date'
    ]
    list_per_page = 20

admin.site.register(Order, OrderAdmin)

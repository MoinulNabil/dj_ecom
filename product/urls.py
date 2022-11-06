from django.urls import path

from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('list-products/', list_products, name='list-products'),
    path('product-details/<str:slug>/', product_details, name='product-details'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('cart-details/', cart_details, name='cart-details'),
    path('products/<str:slug>/', category_products, name='category-products'),
    path('search/', search, name='search'),
]

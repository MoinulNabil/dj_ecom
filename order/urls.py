from django.urls import path

from .views import *

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('complete_payment/', complete_payment, name='complete_payment'),
    path('save-order/<str:transaction_id>/', save_order, name='save-order'),
]
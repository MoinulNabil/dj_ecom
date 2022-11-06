from django.conf import settings
from django.shortcuts import get_object_or_404

from product.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if cart:
            self.cart = cart
        else:
            self.cart = self.session[settings.CART_SESSION_ID] = {}

    def update_cart(self, product_id, quantity, variations=[]):
        product = get_object_or_404(Product, id=product_id)

        self.cart.setdefault(str(product_id), {"quantity": 0, "variations": variations})
        self.cart[str(product_id)]['quantity'] += int(quantity)
        self.cart[str(product_id)]['subtotal'] = float(self.cart[str(product_id)]['quantity'] * product.get_price)

        if self.cart[str(product_id)]['quantity'] < 1:
            del self.cart[str(product_id)]
        
        self.save()

    def __iter__(self):
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            product_id = str(product.id)
            cart[product_id]['product'] = product

            yield self.cart[product_id]

    def get_total(self):
        return sum([product['subtotal'] for product in self.cart.values()])

    def __len__(self):
        return len(self.cart.keys())
    
    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
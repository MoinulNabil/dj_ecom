from .cart import Cart


def is_enough_stock(request, instance, quantity=1):
    cart = Cart(request)
    product_id = str(instance.id)
    enough = True
    
    if product_id in cart.cart.keys():
        if instance.stock < cart.cart.get(product_id).get('quantity') + int(quantity):
            enough = False

    return enough
from functools import reduce
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.conf import settings

from sslcommerz_python.payment import SSLCSession
from decimal import Decimal

from .models import (
    OrderItem,
    Order
)

from .forms import (
    CheckoutForm
)
from cart.cart import Cart


PAYMENT_INFORMATION = {}


def checkout(request):
    form = CheckoutForm()
    cart = Cart(request)

    if len(cart) < 1:
        return redirect("cart-details")

    if request.method == "POST":
        cart = Cart(request)

        status_url = request.build_absolute_uri(reverse("complete_payment"))
        form = CheckoutForm(request.POST)

        if form.is_valid():
            payment = SSLCSession(
                sslc_is_sandbox=True,
                sslc_store_id=settings.SSLC_STORE_ID,
                sslc_store_pass=settings.SSLC_STORE_PASSWORD
                )

            payment.set_urls(
                success_url=status_url,
                fail_url=status_url,
                cancel_url=status_url,
                ipn_url=status_url
            )
            payment.set_product_integration(
                total_amount=Decimal(cart.get_total()),
                product_category="category",
                product_name="name",
                currency='BDT',
                num_of_item=len(cart),
                shipping_method='YES',
            )
            payment.set_customer_info(
                name=form.cleaned_data.get('first_name') + form.cleaned_data.get('last_name'),
                email=form.cleaned_data.get('email'),
                address1=form.cleaned_data.get('address'),
                address2=form.cleaned_data.get('address'),
                city=form.cleaned_data.get('city'),
                postcode=form.cleaned_data.get('zip_code'),
                country='Bangladesh',
                phone=form.cleaned_data.get('phone_number')
            )
            payment.set_shipping_info(
                shipping_to=form.cleaned_data.get('address'),
                address=form.cleaned_data.get('address'),
                city=form.cleaned_data.get('city'),
                postcode=form.cleaned_data.get('zip_code'),
                country='Bangladesh'
            )
            # If you want to post some additional values
            # payment.set_additional_values(value_a='cusotmer@email.com', value_b='portalcustomerid', value_c='1234', value_d='uuid')

            response_data = payment.init_payment()
            status = response_data['status']

            if status != "SUCCESS":
                failled_reason = response_data['failedreason']
                messages.warning(request, failled_reason)
                return redirect('checkout')

            PAYMENT_INFORMATION['first_name'] = form.cleaned_data.get('first_name')
            PAYMENT_INFORMATION['last_name'] = form.cleaned_data.get('last_name')
            PAYMENT_INFORMATION['email'] = form.cleaned_data.get('email')
            PAYMENT_INFORMATION['phone_number'] = form.cleaned_data.get('phone_number')
            PAYMENT_INFORMATION['city'] = form.cleaned_data.get('city')
            PAYMENT_INFORMATION['zip_code'] = form.cleaned_data.get('zip_code')
            PAYMENT_INFORMATION['address'] = form.cleaned_data.get('address')
            PAYMENT_INFORMATION['country'] = form.cleaned_data.get('country')

            return redirect(response_data['GatewayPageURL'])

    context = {
        "form": form
    }
    return render(request, 'checkout.html', context)


@csrf_exempt
@require_POST
def complete_payment(request):
    data = request.POST
    status = data['status']

    if status == "VALID":
        PAYMENT_INFORMATION['transaction_id'] = data['tran_id']
        return redirect('save-order', transaction_id=data['tran_id'])
    
    elif status == "FAILED":
        messages.warning(request, "Sorry. Pyament failled. Please try again with proper information")
        return redirect('checkout')

    elif status == "CANCELLED":
        messages.warning(request, "You have cancelled your payment !!")
        return redirect('checkout')


    return redirect('checkout')


def save_order(request, transaction_id):
    cart = Cart(request)
    total_items = []

    if transaction_id != PAYMENT_INFORMATION.get('transaction_id'):
        return redirect('checkout')

    for product in cart:
        order_item = OrderItem.objects.create(
            product=product['product'],
            price=product['product'].price,
            discount_in_percentage=product['product'].discount_in_percentage,
            quantity=product['quantity'],
            ordered=True
        )
        ordered_product = order_item.product
        ordered_product.stock -= product['quantity']
        ordered_product.save()
        total_items.append(order_item.id)

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        first_name=PAYMENT_INFORMATION['first_name'],
        last_name=PAYMENT_INFORMATION['last_name'],
        email=PAYMENT_INFORMATION['email'],
        phone_number=PAYMENT_INFORMATION['phone_number'],
        transaction_id=transaction_id,
        city=PAYMENT_INFORMATION['city'],
        country=PAYMENT_INFORMATION['country'],
        zip_code=PAYMENT_INFORMATION['zip_code'],
        address=PAYMENT_INFORMATION['address'],
        total=cart.get_total()
    )

    order.order_items.add(*total_items)
    cart.clear()

    send_email_with_pdf(
        Order,
        order.id,
        f"Order invoice from Nabil Shop",
        f"Hey, {PAYMENT_INFORMATION['first_name']}!! Thank you choosing our shop. Find your invoice attached below. Happy Shopping (:",
        [PAYMENT_INFORMATION['email']]
    )

    if request.user.is_authenticated:
        messages.success(request, "Your order has been successfull. !!")
        return redirect("orders")

    else:
        messages.success(request, "Your order has been successfull")
        return redirect("home")


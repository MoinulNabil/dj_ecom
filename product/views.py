from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

from .models import Category, Product
from cart.cart import Cart
from cart.utilities import is_enough_stock


def home(request):
    featured_products = Product.objects.filter(featured=True)
    featured_categories = Category.objects.filter(featured=True)
    context = {
        "featured_products": featured_products,
        "featured_categories": featured_categories
    }
    return render(request, 'home.html', context)


def list_products(request):
    products = Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 6)
    print(paginator.page)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        return redirect('list-products')
    except EmptyPage:
        return redirect('list-products')

    context = {
        "queryset": queryset,
        "paginator": paginator
    }

    return render(request, 'list-products.html', context)


@never_cache
def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    can_update = is_enough_stock(request, product)

    context = {
        "product": product,
        "can_update": can_update
    }
    return render(request, 'product-details.html', context)


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    data = request.POST.copy()
    data.pop('csrfmiddlewaretoken')
    variants = []

    for variation in data:
        variants.append(data.get(variation))

    cart.update_cart(product_id, 1, variants)
    return redirect('cart-details')


def cart_details(request):
    cart = Cart(request)
    update_quantity = request.GET.get('update_quantity', None)
    product_id = request.GET.get('product_id', None)

    if update_quantity and product_id:
        product = get_object_or_404(Product, id=product_id)
        can_update = is_enough_stock(request, product, update_quantity)

        if can_update:
            cart.update_cart(product_id, int(update_quantity))
            return redirect('cart-details')

        else:
            return redirect('cart-details')

    return render(request, 'cart-details.html')


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.category_products.all()
    context = {
        "products": products
    }
    return render(request, 'category-products.html', context)


@require_GET
def search(request):
    search_by = request.GET.get('search_by', None)

    if search_by:
        products = Product.objects.filter(
            Q(title__icontains=search_by) |
            Q(category__title__icontains=search_by)
        )
        return render(request, 'search.html', {"products": products, "search": search_by})

    return redirect('/')

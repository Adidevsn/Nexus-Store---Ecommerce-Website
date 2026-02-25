from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .cart import Cart
from apps.products.models import Product


def cart_detail(request):
    cart = Cart(request)
    items = cart.get_items()
    shipping = Decimal('5.99')
    total = cart.get_total_price() + shipping if items else Decimal('0.00')
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'items': items,
        'shipping': shipping,
        'total': total,
    })


def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)

    if not product.in_stock:
        messages.error(request, f'"{product.name}" is out of stock.')
        return redirect(request.META.get('HTTP_REFERER', 'product_list'))

    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'cart_count': len(cart), 'message': f'"{product.name}" added to cart!'})

    messages.success(request, f'"{product.name}" added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


def cart_remove(request, id):
    cart = Cart(request)
    cart.remove(id)
    messages.info(request, "Item removed from cart.")
    return redirect('cart')


def cart_update(request, id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(id, quantity)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        items = cart.get_items()
        shipping = Decimal('5.99')
        total = cart.get_total_price() + shipping if items else Decimal('0.00')
        return JsonResponse({
            'cart_count': len(cart),
            'subtotal': str(cart.get_total_price()),
            'total': str(total),
        })

    return redirect('cart')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Cart cleared.")
    return redirect('cart')

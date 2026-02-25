import stripe
from decimal import Decimal
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.cart.cart import Cart
from apps.orders.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    cart = Cart(request)
    items = cart.get_items()
    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')
    profile = request.user.profile if hasattr(request.user, 'profile') else None
    shipping = Decimal('5.99')
    total = cart.get_total_price() + shipping
    return render(request, 'payments/checkout.html', {
        'cart': cart,
        'items': items,
        'shipping': shipping,
        'total': total,
        'profile': profile,
    })


@login_required
def create_checkout_session(request):
    if request.method != 'POST':
        return redirect('checkout')

    cart = Cart(request)
    items = cart.get_items()
    if not items:
        return redirect('cart')

    line_items = []
    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': item['name']},
                'unit_amount': int(item['price'] * 100),
            },
            'quantity': item['quantity'],
        })

    line_items.append({
        'price_data': {
            'currency': 'usd',
            'product_data': {'name': 'Shipping'},
            'unit_amount': 599,
        },
        'quantity': 1,
    })

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            customer_email=request.user.email,
            success_url=request.build_absolute_uri('/payments/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/cart/'),
            metadata={
                'user_id': str(request.user.id),
                'address': request.POST.get('address', ''),
                'city': request.POST.get('city', ''),
                'postal_code': request.POST.get('postal_code', ''),
                'phone': request.POST.get('phone', ''),
                'full_name': request.POST.get('full_name', request.user.get_full_name() or request.user.username),
            }
        )
        return redirect(session.url, code=303)
    except stripe.error.StripeError as e:
        messages.error(request, f"Payment error: {str(e)}")
        return redirect('checkout')


def payment_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('home')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.StripeError:
        messages.error(request, "Could not verify payment. Please contact support.")
        return redirect('home')

    # Prevent duplicate orders
    if Order.objects.filter(stripe_session_id=session_id).exists():
        order = Order.objects.get(stripe_session_id=session_id)
        return render(request, 'payments/success.html', {'order': order})

    if session.payment_status == 'paid' and request.user.is_authenticated:
        cart = Cart(request)
        subtotal = cart.get_total_price()
        shipping = Decimal('5.99')
        meta = session.metadata

        order = Order.objects.create(
            user=request.user,
            full_name=meta.get('full_name', request.user.username),
            email=session.customer_details.email or request.user.email,
            phone=meta.get('phone', ''),
            address=meta.get('address', ''),
            city=meta.get('city', ''),
            postal_code=meta.get('postal_code', ''),
            subtotal=subtotal,
            shipping_cost=shipping,
            total=subtotal + shipping,
            stripe_session_id=session_id,
            is_paid=True,
            status='confirmed',
        )

        for item in cart.get_items():
            OrderItem.objects.create(
                order=order,
                product_id=int(item['id']),
                name=item['name'],
                price=item['price'],
                quantity=item['quantity'],
                image=item.get('image', ''),
            )

        # Decrement stock
        from apps.products.models import Product
        for item in cart.get_items():
            try:
                product = Product.objects.get(id=int(item['id']))
                product.stock = max(0, product.stock - item['quantity'])
                product.save()
            except Product.DoesNotExist:
                pass

        cart.clear()
        messages.success(request, f"Order {order.order_number} placed successfully!")
        return render(request, 'payments/success.html', {'order': order})

    return redirect('cart')


def payment_cancel(request):
    messages.warning(request, "Payment was cancelled. Your cart is still saved.")
    return redirect('cart')

from decimal import Decimal


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.effective_price),
                'name': product.name,
                'image': product.image.url if product.image else '',
                'slug': product.slug,
            }
        self.cart[product_id]['quantity'] += quantity
        # Cap at stock
        if self.cart[product_id]['quantity'] > product.stock:
            self.cart[product_id]['quantity'] = product.stock
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            if quantity <= 0:
                del self.cart[product_id]
            else:
                self.cart[product_id]['quantity'] = quantity
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        if 'cart' in self.session:
            del self.session['cart']
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_items(self):
        items = []
        for product_id, item in self.cart.items():
            items.append({
                'id': product_id,
                'name': item['name'],
                'price': Decimal(item['price']),
                'quantity': item['quantity'],
                'image': item.get('image', ''),
                'slug': item.get('slug', ''),
                'total': Decimal(item['price']) * item['quantity'],
            })
        return items

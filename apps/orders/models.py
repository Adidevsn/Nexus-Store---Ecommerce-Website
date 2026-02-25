from django.db import models
from django.contrib.auth.models import User
import random
import string


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped',   'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number      = models.CharField(max_length=20, unique=True, blank=True)
    status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    full_name         = models.CharField(max_length=150)
    email             = models.EmailField()
    phone             = models.CharField(max_length=15, blank=True)
    address           = models.TextField()
    city              = models.CharField(max_length=100)
    postal_code       = models.CharField(max_length=10, blank=True)
    subtotal          = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost     = models.DecimalField(max_digits=6, decimal_places=2, default=5.99)
    total             = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_session_id = models.CharField(max_length=200, blank=True)
    is_paid           = models.BooleanField(default=False)
    created_at        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = 'NX-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    @property
    def status_steps(self):
        steps = ['pending', 'confirmed', 'shipped', 'delivered']
        try:
            current_index = steps.index(self.status)
        except ValueError:
            current_index = -1
        return [(step, i <= current_index) for i, step in enumerate(steps)]


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product  = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    name     = models.CharField(max_length=200)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image    = models.CharField(max_length=500, blank=True)

    @property
    def total_price(self):
        return self.price * self.quantity

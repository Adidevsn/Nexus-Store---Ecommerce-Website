from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'name', 'price', 'quantity', 'image']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ['order_number', 'user', 'total', 'status', 'is_paid', 'created_at']
    list_editable   = ['status']
    list_filter     = ['status', 'is_paid']
    search_fields   = ['order_number', 'user__username', 'email']
    readonly_fields = ['stripe_session_id', 'created_at', 'order_number']
    inlines         = [OrderItemInline]

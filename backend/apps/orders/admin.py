from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'shipping_email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Información del pedido', {
            'fields': ('user', 'status', 'payment_status')
        }),
        ('Datos de envío', {
            'fields': ('shipping_name', 'shipping_email', 'shipping_phone', 'shipping_address', 'shipping_city')
        }),
        ('Totales', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'total')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']
    list_filter = ['order__created_at']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['order', 'product', 'quantity']

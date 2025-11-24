from django.db import models
from django.contrib.auth.models import User
from apps.products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('PROCESSING', 'En Proceso'),
        ('COMPLETED', 'Completado'),
        ('CANCELLED', 'Cancelado'),
    )
    
    SHIPPING_STATUS_CHOICES = (
        ('PENDING', 'Pendiente de envío'),
        ('PREPARING', 'Preparando pedido'),
        ('SHIPPED', 'Enviado'),
        ('IN_TRANSIT', 'En tránsito'),
        ('OUT_FOR_DELIVERY', 'En reparto'),
        ('DELIVERED', 'Entregado'),
        ('FAILED', 'Fallo en entrega'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    
    # Delivery/Shipping fields
    shipping_status = models.CharField(
        max_length=20, 
        choices=SHIPPING_STATUS_CHOICES, 
        default='PENDING',
        verbose_name='Estado de envío'
    )
    tracking_number = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name='Número de seguimiento'
    )
    shipping_address = models.TextField(
        blank=True, 
        verbose_name='Dirección de envío'
    )
    estimated_delivery_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name='Fecha estimada de entrega'
    )
    shipped_date = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Fecha de envío'
    )
    delivered_date = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Fecha de entrega'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tracking_number']),
            models.Index(fields=['shipping_status']),
            models.Index(fields=['-estimated_delivery_date']),
        ]
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - ${self.total}"
    
    def calculate_total(self):
        """Calcula el total sumando todos los items"""
        total = sum(item.subtotal for item in self.items.all())
        self.total = total
        self.save()
        return total
    
    @property
    def is_trackable(self):
        """Verifica si el pedido tiene seguimiento disponible"""
        return bool(self.tracking_number)
    
    @property
    def can_be_delivered(self):
        """Verifica si el pedido está en estado que puede ser entregado"""
        return self.shipping_status in ['SHIPPED', 'IN_TRANSIT', 'OUT_FOR_DELIVERY']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    @property
    def subtotal(self):
        """Calcula el subtotal del item (precio unitario * cantidad)"""
        return self.unit_price * self.quantity

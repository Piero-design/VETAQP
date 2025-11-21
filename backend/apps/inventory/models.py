from django.db import models
from django.contrib.auth.models import User
from apps.products.models import Product


class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
        ('ADJUSTMENT', 'Ajuste'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_movements')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        # Update product stock when movement is saved
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            if self.movement_type == 'IN':
                self.product.stock += self.quantity
            elif self.movement_type == 'OUT':
                self.product.stock -= self.quantity
            elif self.movement_type == 'ADJUSTMENT':
                self.product.stock = self.quantity
            self.product.save()

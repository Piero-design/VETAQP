from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


class Membership(models.Model):
    PLAN_CHOICES = [
        ('BASIC', 'Básico'),
        ('PREMIUM', 'Premium'),
        ('VIP', 'VIP'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('EXPIRED', 'Expirado'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    auto_renew = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_plan_name_display()} ({self.get_status_display()})"
    
    @property
    def days_remaining(self):
        if self.status != 'ACTIVE':
            return 0
        delta = self.end_date - timezone.now().date()
        return max(0, delta.days)
    
    @property
    def is_expired(self):
        return timezone.now().date() > self.end_date
    
    def save(self, *args, **kwargs):
        # Auto-actualizar estado si expiró
        if self.is_expired and self.status == 'ACTIVE':
            self.status = 'EXPIRED'
        super().save(*args, **kwargs)
